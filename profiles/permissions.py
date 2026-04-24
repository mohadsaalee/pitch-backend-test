from rest_framework import permissions
from connections.models import FollowRequest


class CanViewProfile(permissions.BasePermission):
    """
    - Public roles (investor, consultant, ecosystem_partner): anyone can view.
    - Private roles (innovator, startup): only if owner, or follower with accepted request.
    """

    def has_object_permission(self, request, view, obj):
        target_user = obj.user
        if target_user == request.user:
            return True
        if target_user.is_public_profile:
            return True
        # private profile — check accepted follow
        return FollowRequest.objects.filter(
            sender=request.user,
            receiver=target_user,
            status='accepted',
        ).exists()
