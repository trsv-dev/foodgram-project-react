from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Tags, Ingredients, Recipe
from recipes.serializers import (
    TagsSerializer, IngredientsSerializer, RecipesSerializer
)
from recipes.filters import IngrediensByNameSearchFilter


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.AllowAny,)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngrediensByNameSearchFilter


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет создания рецепта."""
    queryset = Recipe.objects.all()
    pass
