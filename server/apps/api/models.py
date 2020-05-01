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
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=30,unique=True)
    nickname = models.CharField(max_length=30, unique=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username


class Clothes(models.Model):

    upper_category = models.CharField(max_length=30, choices=UPPER_CATEGORY_CHOICES)
    lower_category = models.CharField(max_length=30, choices=LOWER_CATEGORY_CHOICES)
    image_url = models.URLField(unique=True)
    alias = models.CharField(max_length=30, null=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class ClothesSet(models.Model):

    clothes = models.ManyToManyField(Clothes)
    name = models.CharField(max_length=30, null=True)
    style = models.CharField(max_length=30, null=True, choices=STYLE_CHOICES)
    image_url = models.URLField(unique=True)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)


class ClothesSetReview(models.Model):

    clothes_set = models.ForeignKey('ClothesSet', on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.IntegerField(choices=LOCATION_CHOICES)
    review = models.IntegerField(choices=REVIEW_CHOICES)
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    max_sensible_temp = models.FloatField()
    min_sensible_temp = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    precipitation = models.FloatField()
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, default='한줄평을 입력해주세요.')
    created_at = models.DateTimeField(default=timezone.now)
    

class Weather(models.Model):
    location_code = models.IntegerField()
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    date = models.DateField()
    time = models.IntegerField(choices=TIME_CHOICES)
    temp = models.FloatField()
    sensible_temp = models.FloatField()
    humidity = models.IntegerField()
    wind_speed = models.FloatField()
    precipitation = models.FloatField()
