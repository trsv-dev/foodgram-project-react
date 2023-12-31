from django.urls import path, include
from rest_framework import routers
from api.views import (
    TagsViewSet, IngredientsViewSet, RecipesViewSet, CustomUserViewSet
)

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('recipes', RecipesViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
