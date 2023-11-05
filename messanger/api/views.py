from django.shortcuts import render

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions

from . import mixins
from main.models import Room, User
from main.serializers import RoomSerializer, UserSerializer, RegisterUserSerializer


class RoomListAPIView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(host=user, participants=[user])
    
room_list_view = RoomListAPIView.as_view()


class RoomCreateApiView(
    generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    def perform_create(self, serializer):
        print(self.request.headers)
        user = self.request.user
        serializer.save(host=user, participants=[user])

room_create_view = RoomCreateApiView.as_view()


class RoomDetailUpdateDeleteAPIView(mixins.IsAuthenticatedEditorMixin, 
                                    generics.RetrieveUpdateDestroyAPIView):
    queryset  = Room.objects.all()
    serializer_class = RoomSerializer

room_detail_update_destroy_view = RoomDetailUpdateDeleteAPIView.as_view()


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

user_list_view = UserListAPIView.as_view()


class UserDetailUpdateDeleteAPIView(
                                    mixins.IsAccountOwnerMixin,
                                    generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

user_detail_update_destroy_view = UserDetailUpdateDeleteAPIView.as_view()


class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]


user_create_view = UserCreateApiView.as_view()

