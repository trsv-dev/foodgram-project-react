from django.contrib import admin

from recipes.models import Ingredients, Tags


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'name', 'measurement_unit'
    )
    list_display_links = ('name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('name', 'measurement_unit')
    ordering = ('id',)
    empty_value_display = '-Пусто-'


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)
    ordering = ('id',)
    prepopulated_fields = {'slug': ('name',)}
    empty_value_display = '-Пусто-'
