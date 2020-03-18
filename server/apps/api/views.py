from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_queryset(self):
        # # This code is to test if request.user is received correctly
        # if self.request.user.is_authenticated:
        #     print(self.request.user)
        return super().get_queryset()
    