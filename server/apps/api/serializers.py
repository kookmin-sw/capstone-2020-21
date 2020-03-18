from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    
    class Meta:
        model = User
        fields = ['id', 'username', 'gender', 'birthday']