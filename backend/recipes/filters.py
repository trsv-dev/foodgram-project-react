from django.db.models import Q, Case, When, Value, CharField
from django_filters import rest_framework as filters
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import ValidationError

from recipes.models import Ingredients, Recipe


class IngrediensByNameSearchFilter(filters.FilterSet):
    """Фильтр поиска по названию ингредиента."""

    name = filters.CharFilter(method='filter_by_name')

    class Meta:
        model = Ingredients
        fields = ('name',)

    def filter_by_name(self, queryset, name, value):
        """
        Фильтрация сначала по первому вхождению,
        а потом по произвольному месту.
        """

        case_expression = Case(
            When(name__istartswith=value, then=Value(1)),
            default=Value(2),
            output_field=CharField(),
        )

        sorted_queryset = queryset.annotate(
            custom_sort=case_expression,
        ).filter(Q(name__istartswith=value) | Q(name__icontains=value))

        return sorted_queryset.order_by(case_expression)


class RecipesFiltering(filters.FilterSet):
    """Фильтр для сортировки выдачи по тегам."""

    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug',
        label='tags',
    )

    is_favorited = filters.BooleanFilter(
        method='get_is_favorited',
        label='favorites',
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'is_favorited')

    def is_user_anonimous(self):
        """
        Проверка на анонимность пользователя.
        Если анонимен, избранного у него быть не может,
        показываем ошибку.
        """

        user = self.request.user
        if isinstance(user, AnonymousUser):
            raise ValidationError(
                f'Вы не можете фильтровать избранное. '
                f'Для такой фильтрации вы должны быть авторизованы.'
            )
        return user

    def get_is_favorited(self, queryset, name, value):
        """Фильтруем избранное."""

        user = self.is_user_anonimous()
        if value:
            return queryset.filter(favorites__user=user)
        return queryset
