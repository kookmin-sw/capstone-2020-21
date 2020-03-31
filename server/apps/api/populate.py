from django.contrib.auth.hashers import make_password
from faker import Faker
from apps.api.factories import (
    UserFactory, ClothesFactory, ClothesSetFactory, ClothesSetReviewFactory
)
from .models import Clothes, ClothesSet

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


def populate_clothes(number=10):
    fake = Faker('ko_KR')

    category_dict = {
        'bottom' : ['shorts', 'hot_pants', 'slacks', 'jeans', 'golden_pants', 'sweatpants'],
        'dress' : ['dress'],
        'outer' : ['blazer', 'short_padding', 'vest_padding', 'long_padding', 'stadium_jacket', 
                    'coach_jacket', 'windbreaker', 'field_jacket', 'mustang', 'coat', 'track_top', 
                    'leather_jacket', 'blue_jacket', 'cardigan', 'dress', ],
        'skirt' : ['skirt', 'long_skirt'],
        'top' : ['short_sleeve', 'long_sleeve', 'short_sleeve_shirt', 'long_sleeve_shirt', 'sweatshirt', 
                'turtleneck', 'hoodie',  'sweater', 'blouse', 'spaghetti_strap', 'sleeveless'] 
    }

    for i in range(number):
        upper_category = fake.random_element(elements=category_dict.keys())
        lower_category = fake.random_element(elements=category_dict[upper_category])
        image_url = fake.image_url(width=None, height=None)
        alias = fake.word(ext_word_list=None)
        created_at = fake.date_time_between(start_date='-90d', end_date='-60d')
        
        created = ClothesFactory.create(
            upper_category=upper_category, 
            lower_category=lower_category, 
            image_url=image_url,
            alias=alias,
            created_at=created_at
        )
        print(created)


def populate_clothes_set(number=10):
    fake = Faker('ko_KR')

    for i in range(number):
        created = ClothesSetFactory.build()

        clothes = Clothes.objects.all().filter(owner_id=created.owner_id)

        clothes_set = set()
        for cloth in clothes:
                clothes_set.add(cloth)

        clothes = fake.random_elements(elements=clothes_set, length=4, unique=True)
        name = fake.word(ext_word_list=None)
        style = fake.random_element(elements=('simple', 'street', 'suit', 'date', 'splendor'))
        image_url = fake.image_url(width=None, height=None)
        created_at = fake.date_time_between(start_date='-60d', end_date='-30d')

        ClothesSetFactory.create(
            name=name, 
            style=style,
            image_url=image_url,
            created_at=created_at,
            clothes=clothes,
            owner_id=created.owner_id
        )
        print(created)


def populate_clothes_set_review(number=10):
    fake = Faker('ko_KR')

    for i in range(number):
        created = ClothesSetReviewFactory.build()

        filtered_clothes_set = ClothesSet.objects.all().filter(owner_id=created.owner_id)
        
        filtered_clothes = set()
        for clothes_set in filtered_clothes_set:
                filtered_clothes.add(clothes_set.id)

        start_datetime = fake.date_time_between(start_date='-30d', end_date='-15d')
        end_datetime = fake.date_time_between(start_date='-15d', end_date='-3d')
        location = fake.pyint(min_value=0, max_value=3379)
        review = fake.random_element(elements=(1, 2, 3, 4, 5))
        max_temp = fake.pyfloat(max_value=35.0, min_value=15.0)
        min_temp = fake.pyfloat(max_value=15.0, min_value=-20.0)
        max_sensible_temp = fake.pyfloat(max_value=35.0, min_value=15.0)
        min_sensible_temp = fake.pyfloat(max_value=15.0, min_value=-20.0)
        humidity = fake.pyint(max_value=100, min_value=0)
        wind_speed = fake.pyint(max_value=150, min_value=0)
        precipitation = fake.pyint(max_value=200, min_value=0)
        comment = fake.image_url(width=None, height=None)
        created_at = fake.date_time_between(start_date='-2d', end_date='now')
        clothes_set_id = fake.random_elements(elements=filtered_clothes, length=1, unique=True)
        
        created = ClothesSetReviewFactory.create(
            start_datetime=start_datetime, 
            end_datetime=end_datetime, 
            location=location,
            review=review,
            max_temp=max_temp,
            min_temp=min_temp,
            max_sensible_temp=max_sensible_temp, 
            min_sensible_temp=min_sensible_temp, 
            humidity=humidity,
            wind_speed=wind_speed,
            precipitation=precipitation,
            comment=comment,
            created_at=created_at,
            clothes_set_id=clothes_set_id,
            owner_id=created.owner_id
        )
        print(created)
