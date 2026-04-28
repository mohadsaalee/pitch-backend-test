from django.contrib.auth import authenticate
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # 🔍 Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not registered")

        # 🔐 Authenticate using email as username
        user = authenticate(username=user.email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid password")

        # 🔑 Generate tokens
        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data
        }

        return data