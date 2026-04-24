from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import FollowRequest, InterestMessage
from .serializers import FollowRequestSerializer, InterestMessageSerializer
from notifications.utils import create_notification

User = get_user_model()


class SendFollowRequestView(generics.CreateAPIView):
    serializer_class = FollowRequestSerializer

    def perform_create(self, serializer):
        follow_req = serializer.save()
        if follow_req.status == 'accepted':
            create_notification(
                recipient=follow_req.receiver,
                sender=follow_req.sender,
                notif_type='follow_accepted',
                message=f'{follow_req.sender.full_name} is now following you.',
            )
        else:
            create_notification(
                recipient=follow_req.receiver,
                sender=follow_req.sender,
                notif_type='follow_request',
                message=f'{follow_req.sender.full_name} sent you a follow request.',
            )


class RespondFollowRequestView(APIView):
    """Accept or reject a follow request received by the current user."""

    def post(self, request, pk):
        follow_req = get_object_or_404(FollowRequest, pk=pk, receiver=request.user, status='pending')
        action = request.data.get('action')  # 'accept' or 'reject'
        if action not in ('accept', 'reject'):
            return Response({'detail': "action must be 'accept' or 'reject'."}, status=400)

        follow_req.status = 'accepted' if action == 'accept' else 'rejected'
        follow_req.save()

        if follow_req.status == 'accepted':
            create_notification(
                recipient=follow_req.sender,
                sender=follow_req.receiver,
                notif_type='follow_accepted',
                message=f'{follow_req.receiver.full_name} accepted your follow request.',
            )
        return Response(FollowRequestSerializer(follow_req, context={'request': request}).data)


class UnfollowView(APIView):
    """Remove an accepted follow relationship."""

    def delete(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)
        deleted, _ = FollowRequest.objects.filter(
            sender=request.user, receiver=target, status='accepted'
        ).delete()
        if deleted:
            return Response({'detail': 'Unfollowed.'}, status=204)
        return Response({'detail': 'No active follow found.'}, status=404)


class MyFollowRequestsView(generics.ListAPIView):
    """Pending requests received by the current user."""
    serializer_class = FollowRequestSerializer

    def get_queryset(self):
        return FollowRequest.objects.filter(receiver=self.request.user, status='pending').select_related('sender', 'receiver')


class MyFollowersView(generics.ListAPIView):
    """Users who follow the current user (accepted)."""
    serializer_class = FollowRequestSerializer

    def get_queryset(self):
        return FollowRequest.objects.filter(receiver=self.request.user, status='accepted').select_related('sender', 'receiver')


class MyFollowingView(generics.ListAPIView):
    """Users the current user follows (accepted)."""
    serializer_class = FollowRequestSerializer

    def get_queryset(self):
        return FollowRequest.objects.filter(sender=self.request.user, status='accepted').select_related('sender', 'receiver')


class SendInterestView(generics.CreateAPIView):
    """Send an interest message — stored in DB and dispatched via email."""
    serializer_class = InterestMessageSerializer

    def perform_create(self, serializer):
        interest = serializer.save(sender=self.request.user)
        self._send_email(interest)

    def _send_email(self, interest):
        try:
            send_mail(
                subject=f'[{settings.PLATFORM_NAME}] Interest: {interest.subject}',
                message=(
                    f'Hello {interest.receiver.full_name},\n\n'
                    f'{interest.sender.full_name} has expressed interest in connecting with you.\n\n'
                    f'Tag: {interest.get_tag_display()}\n'
                    f'Message:\n{interest.message}\n\n'
                    f'To respond, visit {settings.FRONTEND_URL}/profile/{interest.sender.id}\n\n'
                    f'— The {settings.PLATFORM_NAME} Team'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[interest.receiver.email],
                fail_silently=False,
            )
            interest.email_sent = True
            interest.save(update_fields=['email_sent'])
        except Exception:
            pass  # Log in production; don't break the API response

        create_notification(
            recipient=interest.receiver,
            sender=interest.sender,
            notif_type='interest_received',
            message=f'{interest.sender.full_name} sent you an interest message: "{interest.subject}"',
        )


class MyInterestsSentView(generics.ListAPIView):
    serializer_class = InterestMessageSerializer

    def get_queryset(self):
        return InterestMessage.objects.filter(sender=self.request.user).select_related('sender', 'receiver')


class MyInterestsReceivedView(generics.ListAPIView):
    serializer_class = InterestMessageSerializer

    def get_queryset(self):
        return InterestMessage.objects.filter(receiver=self.request.user).select_related('sender', 'receiver')
