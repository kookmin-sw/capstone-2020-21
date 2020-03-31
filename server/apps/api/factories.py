from django.contrib.auth.hashers import make_password
import factory
from faker import Faker

from .models import User

fake = Faker('ko_KR')

class UserFactory(factory.DjangoModelFactory):
    """
    username, password, nickname, gender, birthday
    """
    class Meta:
        model = User
        django_get_or_create = ('username', 'password', 'nickname', 'gender', 'birthday')

