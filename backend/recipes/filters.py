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

        return queryset.filter(name__istartswith=value) | \
               queryset.filter(name__icontains=value)
