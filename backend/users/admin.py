from django.contrib import admin

from users.models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Приложение users."""

    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name'
    )
    list_display_links = ('username', 'email')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    ordering = ('id',)
    empty_value_display = '-Пусто-'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Подписки."""

    list_display = ('author', 'follower')
    list_display_links = ('author', 'follower')
    list_filter = ('author', 'follower')
    ordering = ('author',)
