from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from . import validators
from .signals import user_registered
from .models import Room
from api.serializers import UserInfoSerializer


User = get_user_model()

class RoomSerializer(serializers.ModelSerializer):
    owner = UserInfoSerializer(source='host', read_only=True)
    # room_description = serializers.CharField(source='description')
    participants_count = serializers.IntegerField(source='participants.count', read_only=True)
    messages_count = serializers.IntegerField(source='message_set.all.count', read_only=True)
    participants = serializers.SerializerMethodField(source='get_participants')
    url = serializers.HyperlinkedIdentityField(view_name='room-detail-update-destroy')

    
    class Meta:
        model = Room
        fields = [
            'owner',
            'url',
            'pk',
            'name',
            'description',
            'participants',
            'participants_count',
            'messages_count',
            'updated',
            'created',
        ]
    
    def get_participants(self, obj):
        return [participant.email for participant in obj.participants.all()]
    

class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail-update-destroy')
    rooms = serializers.SerializerMethodField(source='get_rooms', read_only=True)
    messages_count = serializers.IntegerField(source='message_set.all.count', read_only=True)
    superuser = serializers.BooleanField(source='is_superuser', read_only=True)
    staff = serializers.BooleanField(source='is_staff', read_only=True)
    joined = serializers.DateTimeField(source='date_joined', read_only=True)
    last_login = serializers.SerializerMethodField(source='get_last_login', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'url',
            'id',
            'username',
            'email',
            'rooms',
            'messages_count',
            'superuser',
            'staff',
            'joined',
            'last_login',
        ]

    def get_last_login(self, obj):
        return obj.last_login

    def get_rooms(self, obj):
        return [room.name for room in obj.rooms.all()]
    

class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[validators.validate_email])
    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
    
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({'password':'Password field does not match'})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.filter(
                email=validated_data['email'],
                is_active=False,
                last_login=None,
            ).exists()

        if user:
            user = User.objects.get(
                email=validated_data['email'],
                is_active=False,
                last_login=None,)
            user.username = validated_data['username']
        else:
            user = User.objects.create(
                email=validated_data['email'],
                username=validated_data['username'],
                is_active = False
                )

        user.set_password(validated_data['password1'])
        user.save()

        user_registered.send(sender=User, instance=user)

        return user
    

