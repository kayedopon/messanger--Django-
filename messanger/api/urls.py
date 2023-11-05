from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('rooms/', views.room_list_view, name='room-list'),
    path('rooms/create/', views.room_create_view, name='room-create'),
    path('rooms/<int:pk>/', views.room_detail_update_destroy_view, name='room-detail-update-destroy'),
    path('users/', views.user_list_view, name='user-list'),
    path('users/create/', views.user_create_view, name='user-create'),
    path('users/<int:pk>/', views.user_detail_update_destroy_view, name='user-detail-update-destroy')
]
