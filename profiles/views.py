from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PROFILE_SERIALIZER_MAP, PROFILE_MODEL_MAP
from .permissions import CanViewProfile

User = get_user_model()


class MyProfileView(APIView):
    """GET/PATCH the current user's own profile."""

    def _get_profile_and_serializer(self, user):
        model = PROFILE_MODEL_MAP.get(user.role)
        serializer_class = PROFILE_SERIALIZER_MAP.get(user.role)
        if not model:
            return None, None, None
        profile, _ = model.objects.get_or_create(user=user)
        return profile, serializer_class, model

    def get(self, request):
        profile, serializer_class, _ = self._get_profile_and_serializer(request.user)
        if not profile:
            return Response({'detail': 'Unknown role.'}, status=400)
        return Response(serializer_class(profile).data)

    def patch(self, request):
        profile, serializer_class, _ = self._get_profile_and_serializer(request.user)
        if not profile:
            return Response({'detail': 'Unknown role.'}, status=400)
        serializer = serializer_class(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Mark profile complete if key fields filled
        self._check_completeness(profile, request.user.role)
        return Response(serializer.data)

    def _check_completeness(self, profile, role):
        complete = False
        if role == 'innovator':
            complete = bool(profile.bio and profile.skills)
        elif role == 'startup':
            complete = bool(profile.company_name and profile.industry and profile.bio)
        elif role == 'investor':
            complete = bool(profile.bio and profile.sectors_of_interest)
        elif role == 'consultant':
            complete = bool(profile.bio and profile.expertise)
        elif role == 'ecosystem_partner':
            complete = bool(profile.organization_name and profile.organization_type)
        if complete != profile.is_profile_complete:
            profile.is_profile_complete = complete
            profile.save(update_fields=['is_profile_complete'])


class UserProfileView(APIView):
    """View any user's profile (privacy enforced)."""
    permission_classes = [permissions.IsAuthenticated, CanViewProfile]

    def get(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        model = PROFILE_MODEL_MAP.get(target.role)
        serializer_class = PROFILE_SERIALIZER_MAP.get(target.role)
        if not model:
            return Response({'detail': 'Profile type unknown.'}, status=400)
        profile = get_object_or_404(model, user=target)
        self.check_object_permissions(request, profile)
        return Response(serializer_class(profile).data)


class PublicProfilesListView(APIView):
    """List all public-role profiles (investors, consultants, ecosystem partners)."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        role = request.query_params.get('role')
        public_roles = ['investor', 'consultant', 'ecosystem_partner']
        if role and role not in public_roles:
            return Response({'detail': 'Only public role profiles are listable.'}, status=400)

        results = []
        roles_to_query = [role] if role else public_roles
        for r in roles_to_query:
            model = PROFILE_MODEL_MAP[r]
            serializer_class = PROFILE_SERIALIZER_MAP[r]
            for profile in model.objects.select_related('user').all():
                data = serializer_class(profile).data
                data['role'] = r
                results.append(data)
        return Response(results)
