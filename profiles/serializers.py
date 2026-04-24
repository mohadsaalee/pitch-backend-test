from rest_framework import serializers
from .models import (
    InnovatorProfile, StartupProfile, InvestorProfile,
    ConsultantProfile, EcosystemPartnerProfile,
)


class InnovatorProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = InnovatorProfile
        exclude = ['user']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StartupProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = StartupProfile
        exclude = ['user']
        read_only_fields = ['id', 'created_at', 'updated_at']


class InvestorProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = InvestorProfile
        exclude = ['user']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConsultantProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = ConsultantProfile
        exclude = ['user']
        read_only_fields = ['id', 'created_at', 'updated_at']


class EcosystemPartnerProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = EcosystemPartnerProfile
        exclude = ['user']
        read_only_fields = ['id', 'created_at', 'updated_at']


PROFILE_SERIALIZER_MAP = {
    'innovator': InnovatorProfileSerializer,
    'startup': StartupProfileSerializer,
    'investor': InvestorProfileSerializer,
    'consultant': ConsultantProfileSerializer,
    'ecosystem_partner': EcosystemPartnerProfileSerializer,
}

PROFILE_MODEL_MAP = {
    'innovator': InnovatorProfile,
    'startup': StartupProfile,
    'investor': InvestorProfile,
    'consultant': ConsultantProfile,
    'ecosystem_partner': EcosystemPartnerProfile,
}
