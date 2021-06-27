from django.db.models import fields
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    position = serializers.CharField()
    gender = serializers.CharField()
    date_of_birth = serializers.DateField()

class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()