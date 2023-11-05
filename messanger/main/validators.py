from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

def validate_email(value):
    if User.objects.filter(email=value, is_active=False).exists():
        return value
    elif User.objects.filter(email=value).exists():
        raise serializers.ValidationError("User with this email already exists.")
    
    return value