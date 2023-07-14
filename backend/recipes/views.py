from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Tags, Ingredients
from recipes.serializers import TagsSerializer, IngredientsSerializer
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
