from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password before saving
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return Profile.objects.create(**validated_data)