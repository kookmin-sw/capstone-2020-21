from rest_framework import serializers
from .models import User, Clothes, ClothesSet, ClothesSetReview

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'nickname', 'gender', 'birthday']
        extra_kwargs = {'password': {'write_only': True}}


class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = ('id', 'upper_category', 'lower_category', 'image_url', 'alias', 'owner')
        

class ClothesSetSerializer(serializers.ModelSerializer):
    clothes = ClothesSerializer(many=True)
    
    class Meta:
        model = ClothesSet
        fields = ('id', 'clothes', 'name', 'style', 'image_url', 'owner')
        

class ClothesSetReviewSerializer(serializers.ModelSerializer):
    clothes_set = ClothesSetSerializer()
    
    class Meta:
        model = ClothesSetReview
        fields = ('id', 'clothes_set', 'start_datetime', 'end_datetime', 
                  'location', 'review', 'max_temp', 'min_temp', 
                  'max_sensible_temp', 'min_sensible_temp', 'humidity', 
                  'wind_speed', 'precipitation', 'comment', 'owner')
        
