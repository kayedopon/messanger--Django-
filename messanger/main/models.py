from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager

from datetime import timedelta

# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, email, username, password, **extra_fields):
        if not username:
            raise ValueError("You must have a username")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(email, username, password, **extra_fields)
    

class User(AbstractUser):
    username = models.CharField(unique=False, max_length=30)
    email = models.EmailField(unique=True, max_length=50)
    avatar = models.ImageField(null=True, default='avatar.svg')
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self) -> str:
        return self.email
    
    
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length=200)
    avatar = models.ImageField(null=True, default='avatar.svg')
    description = models.TextField(max_length=50, null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='rooms', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ['-updated',]
    
    def __str__(self) -> str:
            return self.name
    
class Message(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self) -> str:
        return self.body[0:20]