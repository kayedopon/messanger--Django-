from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('register/verification/', views.preVerification, name='pre-verification'),
    path('register/verification/<str:signing>/', views.verification, name='verification'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.home, name='home'),
    path('room/<int:id>/', views.room, name='room'),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)