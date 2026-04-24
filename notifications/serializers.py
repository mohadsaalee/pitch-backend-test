from rest_framework import serializers
from .models import Notification
from users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.full_name', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'sender_name', 'notif_type', 'message', 'is_read', 'created_at']
        read_only_fields = fields
