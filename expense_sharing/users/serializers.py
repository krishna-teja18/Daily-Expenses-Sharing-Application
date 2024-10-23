from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile_number', 'password']

    def validate_mobile_number(self, value):
        if not value.startswith('+91') and len(value) != 13:
            raise serializers.ValidationError("Invalid Indian mobile number format. It should start with +91.")
        return value

    def validate_email(self, value):
        if '@' not in value or '.' not in value.split('@')[-1]:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def create(self, validated_data):
        # Hash the password before saving for security
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
