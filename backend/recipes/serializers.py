from rest_framework import serializers

from recipes.models import Tags


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов."""

    class Meta:
        model = Tags
        fields = ('name', 'color', 'slug')
