from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from .models import Clothes, ClothesSet, ClothesSetReview, User
from .serializers import (
    ClothesSerializer,
    ClothesSetSerializer,
    ClothesSetReviewSerializer,
    UserSerializer
)

class UserView(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        """
        A endpoint where current user's data is returned,
        uses Authorization JWT token to check the user.
        """
        if self.request.user.is_authenticated:
            self.kwargs.update(pk=request.user.id)
            return self.retrieve(request, *args, **kwargs)
        else:
            return Response(
                {'error': 'please log in'},
                status=status.HTTP_401_UNAUTHORIZED)
    

class ClothesView(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Clothes.objects.all()
    serializer_class = ClothesSerializer
    

class ClothesSetView(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ClothesSet.objects.all()
    serializer_class = ClothesSetSerializer
    
    
class ClothesSetReviewView(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = ClothesSetReview.objects.all()
    serializer_class = ClothesSetReviewSerializer
    
    