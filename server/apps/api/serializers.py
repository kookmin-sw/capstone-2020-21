from rest_framework import serializers
from .models import User, Clothes, ClothesSet, ClothesSetReview


# test git commit
class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    
    class Meta:
        model = User
        fields = ['id', 'username', 'gender', 'birthday']


class ClothesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothes
        fields = ('id', 'upper_category', 'lower_category', 'image_url', 'alias', 'owner')
        

class ClothesSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesSet
        fields = ('id', 'clothes', 'name', 'style', 'image_url', 'owner')
        

class ClothesSetReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothesSetReview
        fields = ('id', 'clothes_set', 'start_datetime', 'end_datetime', 
                  'location', 'review', 'max_temp', 'min_temp', 
                  'max_sensible_temp', 'min_sensible_temp', 'humidity', 
                  'wind_speed', 'precipitation', 'owner')
        
