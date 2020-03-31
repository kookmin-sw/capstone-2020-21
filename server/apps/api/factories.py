from django.contrib.auth.hashers import make_password
import factory
from faker import Faker

from .models import User, Clothes, ClothesSet, ClothesSetReview

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
