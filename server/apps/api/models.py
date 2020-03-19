from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .choices import *
from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    
    birthday = models.DateField(null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    gender = models.BooleanField(null=True, choices=GENDER_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=30,unique=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username


class Clothes(models.Model):

    upper_category = models.IntegerField(max_length=30, choices=UPPER_CATEGORY_CHOICES)
    lower_category = models.IntegerField(max_length=30, choices=LOWER_CATEGORY_CHOICES)
    image_url = models.URLField(unique=True)
    alias = models.CharField(max_length=30, null=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)


class ClothesSet(models.Model):

    chothes = models.ManyToManyField(Clothes)
    name = models.CharField(max_length=30)
    style = models.CharField(max_length=30)
    image_url = models.URLField(unique=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)


class ClothesSetReview(models.Model):

    clothes_set = models.ForeignKey('ClothesSet', on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.IntegerField(max_length=50, choices=LOCATION_CHOICES)
    review = models.IntegerField(max_length=30, choices=REVIEW_CHOICES)
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    max_sensible_temp = models.FloatField()
    min_sensible_temp = models.FloatField()
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    precipitation = models.IntegerField()
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    
