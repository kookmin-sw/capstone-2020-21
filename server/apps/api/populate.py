from django.contrib.auth.hashers import make_password
from faker import Faker
from apps.api.factories import (
    UserFactory, ClothesFactory, ClothesSetFactory, ClothesSetReviewFactory
)
from .models import User, Clothes, ClothesSet

def populate_users(number=10):
    fake = Faker('ko_KR')

    created_users = []

    for i in range(number):
        while True:
            username = fake.user_name()
            if len(User.objects.all().filter(username=username)) == 0:
                break
        
        while True:
            nickname = fake.name()
            if len(User.objects.all().filter(nickname=nickname)) == 0:
                break
                
        password = make_password(''.join(fake.random_letters(length=8)))
        gender = fake.random_element(elements=('남자','여자'))
        birthday = fake.date_between(start_date='-30y', end_date='-20y')
        
        created = UserFactory.create(
            username=username, 
            password=password, 
            nickname=nickname,
            gender=gender,
            birthday=birthday
        )
        
        created_users.append(created)
        
    return created_users


def populate_clothes(number=10):
    fake = Faker('ko_KR')

    category_dict = {
        '하의' : ['반바지', '핫팬츠', '슬랙스', '청바지', '골덴바지', '트레이닝바지'],
        '원피스' : ['원피스'],
        '아우터' : ['블레이져', '숏패딩', '조끼패딩', '롱패딩', '야구점퍼', 
                    '항공점퍼', '바람막이', '야상', '무스탕', '코트', '트랙탑', 
                    '가죽자켓', '청자켓', '가디건'],
        '치마' : ['미니스커트', '롱스커트'],
        '상의' : ['반팔티셔츠', '긴팔티셔츠', '반팔셔츠', '긴팔셔츠', '맨투맨', 
                '터틀넥', '후드티',  '니트', '블라우스', '끈나시', '민소매'] 
    }

    created_clothes = []
    users = User.objects.all()
    
    for i in range(number):
        user_index = fake.pyint(min_value=0, max_value=len(users)-1)
        owner = users[user_index]
            
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
            created_at=created_at,
            owner=owner
        )
        
        created_clothes.append(created)
        
    return created_clothes


def populate_clothes_set(number=10):
    fake = Faker('ko_KR')

    created_clothes_set = []
    users = User.objects.all()

    for i in range(number):
        while True:
            user_index = fake.pyint(min_value=0, max_value=len(users)-1)
            owner = users[user_index]
            clothes = Clothes.objects.all().filter(owner_id=owner.id)
            if len(clothes) != 0:
                break

        clothes_set = set()
        for cloth in clothes:
                clothes_set.add(cloth)

        clothes = fake.random_elements(elements=clothes_set, length=4, unique=True)
        name = fake.word(ext_word_list=None)
        style = fake.random_element(elements=('심플', '스트릿', '정장', '데이트', '화려'))
        image_url = fake.image_url(width=None, height=None)
        created_at = fake.date_time_between(start_date='-60d', end_date='-30d')

        created = ClothesSetFactory.create(
            name=name, 
            style=style,
            image_url=image_url,
            created_at=created_at,
            clothes=clothes,
            owner=owner
        )
        
        created_clothes_set.append(created)
        
    return created_clothes_set


def populate_clothes_set_review(number=10):
    fake = Faker('ko_KR')

    created_reviews = []

    users = User.objects.all()
    for i in range(number):
        while True:
            user_index = fake.pyint(min_value=0, max_value=len(users)-1)
            owner = users[user_index]
            filtered_clothes_set = ClothesSet.objects.all().filter(owner_id=owner.id)
            if len(filtered_clothes_set) != 0:
                break
        
        filtered_clothes = []
        for clothes_set in filtered_clothes_set:
                filtered_clothes.append(clothes_set.id)

        clothes_set_key = fake.random_elements(elements=filtered_clothes, length=len(filtered_clothes), unique=True)
        clothes_set_id = clothes_set_key[0]
        
        start_datetime = fake.date_time_between(start_date='-30d', end_date='-15d')
        end_datetime = fake.date_time_between(start_date='-15d', end_date='-3d')
        location = fake.pyint(min_value=0, max_value=3379)
        review = fake.random_element(elements=(1, 2, 3, 4, 5))
        max_temp = fake.pyfloat(max_value=35.0, min_value=15.0, right_digits=1)
        min_temp = fake.pyfloat(max_value=15.0, min_value=-20.0, right_digits=1)
        max_sensible_temp = fake.pyfloat(max_value=35.0, min_value=15.0, right_digits=1)
        min_sensible_temp = fake.pyfloat(max_value=15.0, min_value=-20.0, right_digits=1)
        humidity = fake.pyint(max_value=100, min_value=0)
        wind_speed = fake.pyfloat(max_value=20, min_value=0, right_digits=1)
        precipitation = fake.pyint(max_value=200, min_value=0)
        comment = fake.text(max_nb_chars=100)
        created_at = fake.date_time_between(start_date='-2d', end_date='now')

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
            owner=owner
        )
        
        created_reviews.append(created)
        
    return created_reviews


def populate_database(users=10, clothes=300, clothes_set=50, clothes_set_review=100):
    print('Creating ', users, ' Users ... ')
    populate_users(users)
    print('Created ', users, ' Users !\n')
    

    print('Creating ', clothes, ' Clothes ... ')
    populate_clothes(clothes)
    print('Created ', clothes, ' Clothes !\n')

    print('Creating ', clothes_set, ' ClothesSets ... ')
    populate_clothes_set(clothes_set)
    print('Created ', clothes_set, ' ClothesSets !\n')

    print('Creating ', clothes_set_review, ' ClothesSetReviews ... ')
    populate_clothes_set_review(clothes_set_review)
    print('Created ', clothes_set_review, ' ClothesSetReviews !')

