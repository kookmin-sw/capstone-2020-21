from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    birthday = models.DateTimeField(null=True)
    
    GENDER_CHOICES = [
        (True, 'Man'),
        (False, 'Woman'),
    ]
    gender = models.BooleanField(null=True, choices=GENDER_CHOICES)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
# Create your models here.

class Clothes(models.Model):

    UPPER_CATEGORY_CHOICES = [
        (1, 'Top'),
        (2, 'Bottom'),
        (3, 'Outer'),
        (4, 'Dress'),
        (5, 'Skirt'),
    ]

    LOWER_CATEGORY_CHOICES = [
        (1, 'Jeans'),
        (2, 'Knitwear'),
        (3, 'Jacket')
    ]

    upper_category = models.CharField(max_length=10, choices=UPPER_CATEGORY_CHOICES)
    lower_category = models.CharField(max_length=20, choices=LOWER_CATEGORY_CHOICES)
    image_url = models.URLField(unique=True)
    alias = models.CharField(max_length=20, null=True)
    # owner = models.ForeignKey('Users', on_delete=models.CASCADE)


# class ClothesSet(models.Model):


