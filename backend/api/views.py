from django.db.models import Sum, Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import permissions, status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAdmin, IsAuthor
from api.serializers import (
    TagsSerializer, IngredientsSerializer, RecipeIngredient,
    RecipesWriteSerializer, AddToFavoritesSerializer,
    ShortRecipeSerializer, ShoppingListSerializer, RecipesReadSerializer
)
from api.serializers import (
    UserSerializer, FollowSerializer, FollowingStatusSerializer
)
from api.utils import create_shopping_cart
from recipes.filters import RecipesFiltering
from recipes.models import Tags, Ingredients, Recipe, Favorites, ShoppingList
from users.models import User, Follow


class CustomUserViewSet(UserViewSet):
    """Вьюсет создания пользователя."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=True, methods=['POST'], url_path='subscribe',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_subscribe(self, request, id=None):
        """Подписка на автора."""

        follower = request.user
        author = get_object_or_404(User, id=id)

        follow_serializer = FollowSerializer(
            data={'follower': follower.id, 'author': author.id}
        )
        follow_serializer.is_valid(raise_exception=True)
        follow_serializer.save()
        author_serializer = FollowingStatusSerializer(
            author, context={'request': request}
        )
        return Response(
            author_serializer.data, status=status.HTTP_201_CREATED
        )

    @get_subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        """Отписка от автора."""

        follower = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'DELETE':
            del_count, _ = Follow.objects.filter(
                follower=follower, author=author
            ).delete()

            if del_count:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(
        detail=False, methods=['GET'], url_path='subscriptions',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_subscriptions(self, request):
        """Возвращает авторов, на которых подписан пользователь."""

        user = request.user
        queryset = User.objects.filter(author__follower=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowingStatusSerializer(
            pages, context={'request': request}, many=True
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=False, methods=['GET'], url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me(self, request):
        """Получение информации о себе."""

        serializer = UserSerializer(
            instance=request.user,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод ингредиентов."""

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод тэгов."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    permission_classes = (permissions.AllowAny,)


class BaseRecipeView:
    """
    Базовый класс рецептов для наследования RecipesViewSet с общей логикой
    добавления / удаления избранного и элементов корзины.
    """

    @staticmethod
    def add_or_remove_to_favorites_or_cart(
            request, pk, model_class, serializer_class
    ):
        """
        Общий метод для добавления / удаления в
        избранное или в корзину покупок.
        """

        recipe = get_object_or_404(Recipe, pk=pk)

        if request.method == 'DELETE':
            del_count, _ = model_class.objects.filter(
                user=request.user, recipe=recipe
            ).delete()
            if del_count:
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializer_class(
            data={'user': request.user.id, 'recipe': recipe.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        action_serializer = ShortRecipeSerializer(recipe)
        return Response(
            action_serializer.data, status=status.HTTP_201_CREATED
        )


class RecipesViewSet(viewsets.ModelViewSet, BaseRecipeView):
    """Вьюсет для создания объектов класса Recipe."""

    serializer_class = RecipesWriteSerializer
    permission_classes = ((IsAuthor | IsAdmin),)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFiltering

    def get_queryset(self):
        """
        Получение оптимизированного queryset
        с аннотациями и подзапросами.
        """

        if self.request.user.is_authenticated:
            queryset = Recipe.objects.annotate(
                is_favorited=Exists(Favorites.objects.filter(
                    user=self.request.user,
                    recipe_id=OuterRef('pk'),
                )),
                is_in_shopping_cart=Exists(ShoppingList.objects.filter(
                    user=self.request.user,
                    recipe_id=OuterRef('pk'),
                ))
            ).select_related('author')

            return queryset

    @action(
        detail=True, methods=['POST'], url_path='favorite',
        url_name='favorite', permission_classes=(permissions.IsAuthenticated,)
    )
    def get_favorite(self, request, pk):
        """Добавление рецепта в избранное."""

        return self.add_or_remove_to_favorites_or_cart(
            request, pk, Favorites, AddToFavoritesSerializer
        )

    @get_favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """Удаление рецепта из избранного."""

        return self.add_or_remove_to_favorites_or_cart(
            request, pk, Favorites, AddToFavoritesSerializer
        )

    @action(
        detail=True, methods=['POST'], url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_shopping_cart(self, request, pk):
        """
        Позволяет текущему пользователю добавлять рецепты
        в список покупок.
        """

        return self.add_or_remove_to_favorites_or_cart(
            request, pk, ShoppingList, ShoppingListSerializer
        )

    @get_shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Удаление рецепта из списка покупок."""

        return self.add_or_remove_to_favorites_or_cart(
            request, pk, ShoppingList, ShoppingListSerializer
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

        file_to_download = create_shopping_cart(username, ingredients)

        response = HttpResponse(
            file_to_download, content_type='application/pdf'
        )
        response['Content-Disposition'] = \
            f'attachment; filename="{username}_download_list.pdf"'

        return response

    def get_serializer_class(self):
        """Выбор сериализатора для чтения рецепта и редактирования."""

        if self.request.method == 'GET':
            return RecipesReadSerializer
        return RecipesWriteSerializer
