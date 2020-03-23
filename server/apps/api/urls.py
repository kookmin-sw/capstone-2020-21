from django.conf.urls import url, include
from . import views
from rest_framework import routers
from rest_framework_extensions.routers import ExtendedDefaultRouter

# Nested router ref
# https://chibisov.github.io/drf-extensions/docs/#nested-routes
router = ExtendedDefaultRouter()

# Nested router for user.
user_router = router.register('users', views.UserView, basename='users')
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

clothes_router = router.register('clothes', views.ClothesView, basename='clothes')
clothes_router.register('clothes-sets',
                        views.ClothesSetView,
                        basename='clothes-clothes_sets',
                        parents_query_lookups=['clothes'])

clothes_sets_router = router.register('clothes-sets', views.ClothesSetView, basename='clothes-sets')
clothes_sets_router.register('clothes-set-reviews',
                             views.ClothesSetReviewView,
                             basename='clothes_sets-clothes_set_reviews',
                             parents_query_lookups=['clothes_set'])

router.register('clothes-set-reviews', views.ClothesSetReviewView, basename='clothes-set-reviews')

urlpatterns = [
    url('', include(router.urls)),
]
