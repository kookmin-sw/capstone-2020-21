from django.contrib.auth.hashers import make_password
import factory
from faker import Faker

from .models import User, Clothes, ClothesSet, ClothesSetReview, Weather

fake = Faker('ko_KR')

class UserFactory(factory.DjangoModelFactory):
    """
    username, password, nickname, gender, birthday
    """
    class Meta:
        model = User
        django_get_or_create = ('username', 'password', 'nickname', 'gender', 'birthday')


class ClothesFactory(factory.DjangoModelFactory):
    """
    upper_category, lower_category, image_url, alias, owner, created_at
    """
    class Meta:
        model = Clothes
        django_get_or_create = ('upper_category', 'lower_category', 'image_url', 'alias', 'owner', 'created_at')
        
    owner = factory.Iterator(User.objects.all())

class ClothesSetFactory(factory.DjangoModelFactory):
    """
    clothes, name, style, image_url, owner, created_at
    """
    class Meta:
        model = ClothesSet
        django_get_or_create = ('name', 'style', 'image_url', 'owner', 'created_at')
        
    @factory.post_generation
    def clothes(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for cloth in extracted:
                self.clothes.add(cloth)
    

class ClothesSetReviewFactory(factory.DjangoModelFactory):
    """
    start_datetime, end_datetime, location, review, max_temp, min_temp, 
    max_sensible_temp, min_sensible_temp, humidity, wind_speed, precipitation, 
    owner, comment, created_at
    """
    class Meta:
        model = ClothesSetReview
        django_get_or_create = ('start_datetime', 'end_datetime', 'location', 'review', 'owner', 'max_temp', 
                                'min_temp', 'max_sensible_temp', 'min_sensible_temp', 'humidity', 'wind_speed', 
                                'precipitation', 'comment', 'created_at'
                                )
        
class WeatherFactory(factory.DjangoModelFactory):
    """
    location_code, date, time, temp, sensible_temp, humidity, wind_speed, precipitation, x, y
    """
    class Meta:
        model = Weather
        django_get_or_create = ('location_code', 'date', 'time', 'temp', 'sensible_temp', 'humidity', 
                                'wind_speed', 'precipitation', 'x', 'y'
                                )
    
