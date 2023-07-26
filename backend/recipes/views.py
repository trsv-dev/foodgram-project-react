from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAdmin, IsAuthor
from api.serializers import (
    TagsSerializer, IngredientsSerializer, RecipeIngredient,
    RecipesWriteSerializer, AddToFavoritesSerializer,
    AddedRecipeSerializer, ShoppingListSerializer, RecipesReadSerializer
)
from api.utils import create_shopping_cart
from recipes.filters import IngrediensByNameSearchFilter, RecipesFiltering
from recipes.models import Tags, Ingredients, Recipe, Favorites, ShoppingList


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод ингредиентов."""

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngrediensByNameSearchFilter


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод тэгов."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания объектов класса Recipe."""

    queryset = Recipe.objects.select_related('author')
    serializer_class = RecipesWriteSerializer
    permission_classes = ((IsAuthor | IsAdmin),)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFiltering

    @action(detail=True, methods=['POST', 'DELETE'], url_path='favorite',
            url_name='favorite',
            permission_classes=(permissions.IsAuthenticated,)
            )
    def get_favorite(self, request, pk):
        """Позволяет текущему пользователю добавлять рецепты в избранное."""

        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'DELETE':
            favorite_recipe = get_object_or_404(
                Favorites, user=request.user, recipe=recipe
            )
            favorite_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = AddToFavoritesSerializer(
            data={'user': request.user.id, 'recipe': recipe.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        favorite_serializer = AddedRecipeSerializer(recipe)
        return Response(
            favorite_serializer.data, status=status.HTTP_201_CREATED
        )

    @action(
        detail=True, methods=['POST', 'DELETE'], url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_shopping_cart(self, request, pk):
        """
        Позволяет текущему пользователю добавлять рецепты
        в список покупок.
        """

        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'DELETE':
            shopping_cart_recipe = get_object_or_404(
                ShoppingList, user=request.user, recipe=recipe
            )
            shopping_cart_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = ShoppingListSerializer(
            data={'user': request.user.id, 'recipe': recipe.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        shopping_cart_serializer = AddedRecipeSerializer(recipe)
        return Response(
            shopping_cart_serializer.data, status=status.HTTP_201_CREATED
        )

    @action(
        detail=False, methods=['GET'], url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        """Скачивание списка покупок, если он есть."""

        if not request.user.shopping_list.exists():
            return Response({'errors': 'Корзина пуста'},
                            status=status.HTTP_400_BAD_REQUEST)

        username = request.user.username
        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_list__user=request.user
        ).order_by(
            'ingredient__name'
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total_amount=Sum('amount'))

        return create_shopping_cart(username, ingredients)

    def get_serializer_class(self):
        """Выбор сериализатора для чтения рецепта и редактирования."""

        if self.request.method == 'GET':
            return RecipesReadSerializer
        return RecipesWriteSerializer
