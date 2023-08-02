from rest_framework.pagination import PageNumberPagination


class ShoppingCartPagination(PageNumberPagination):
    """Кастомная пагинация для отображения 999 элементов корзины."""

    page_size_query_param = 'limit'
