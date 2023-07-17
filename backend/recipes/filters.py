from django.db.models import Q, Case, When, Value, CharField
from django_filters import rest_framework as filters

from recipes.models import Ingredients


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
