from django.contrib.auth.hashers import make_password
from faker import Faker
from apps.api.factories import UserFactory

def populate_users(number=10):
    fake = Faker('ko_KR')

    for i in range(number):
        username = fake.user_name()
        password = make_password(''.join(fake.random_letters(length=8)))
        nickname = fake.name()
        gender = fake.random_element(elements=(True,False))
        birthday = fake.date_between(start_date='-30y', end_date='-20y')
        
        created = UserFactory.create(
            username=username, 
            password=password, 
            nickname=nickname,
            gender=gender,
            birthday=birthday)
        print(created)
