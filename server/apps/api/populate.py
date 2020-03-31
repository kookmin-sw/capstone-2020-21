from django.contrib.auth.hashers import make_password
from faker import Faker
from apps.api.factories import (
    UserFactory, ClothesFactory, ClothesSetFactory
)
from .models import Clothes

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
        created_at = fake.date_between(start_date='-90d', end_date='-60d')
        
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

