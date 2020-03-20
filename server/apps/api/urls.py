from django.conf.urls import url, include
from . import views
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedDefaultRouter

# Nested router ref
# https://chibisov.github.io/drf-extensions/docs/#nested-routes
router = ExtendedDefaultRouter()

# Nested router for user.
user_router = router.register('users', views.UserView)
user_router.register('clothes',
                     views.ClothesView,
                     basename='user-clothes',
                     parents_query_lookups=['owner'])
user_router.register('clothes-sets',
                     views.ClothesSetView,
                     basename='user-clothes_sets',
                     parents_query_lookups=['owner'])
user_router.register('clothes-set-reviews',
                     views.ClothesSetReviewView,
                     basename='user-clothes_set_reviews',
                     parents_query_lookups=['owner'])

router.register('clothes', views.ClothesView)
router.register('clothes-sets', views.ClothesSetView)
router.register('clothes-set-reviews', views.ClothesSetReviewView)

urlpatterns = [
    url('', include(router.urls)),
]
