from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import FollowRequest, InterestMessage

User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'role']


class FollowRequestSerializer(serializers.ModelSerializer):
    sender = UserMiniSerializer(read_only=True)
    receiver = UserMiniSerializer(read_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='receiver'
    )

    class Meta:
        model = FollowRequest
        fields = ['id', 'sender', 'receiver', 'receiver_id', 'status', 'message', 'created_at']
        read_only_fields = ['id', 'sender', 'status', 'created_at']

    def validate(self, attrs):
        sender = self.context['request'].user
        receiver = attrs['receiver']
        if sender == receiver:
            raise serializers.ValidationError('Cannot follow yourself.')
        if FollowRequest.objects.filter(sender=sender, receiver=receiver).exists():
            raise serializers.ValidationError('Follow request already sent.')
        return attrs

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        # Public profiles: auto-accept
        if validated_data['receiver'].is_public_profile:
            validated_data['status'] = 'accepted'
        return super().create(validated_data)


class InterestMessageSerializer(serializers.ModelSerializer):
    sender = UserMiniSerializer(read_only=True)
    receiver = UserMiniSerializer(read_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='receiver'
    )

    class Meta:
        model = InterestMessage
        fields = ['id', 'sender', 'receiver', 'receiver_id', 'tag', 'subject', 'message', 'email_sent', 'created_at']
        read_only_fields = ['id', 'sender', 'email_sent', 'created_at']
