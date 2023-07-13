from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from users.models import User, Follow


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        username = data.get('username')

        if username == 'me':
            raise ValidationError(
                f"Имя пользователя '{username}' зарезервировано в системе"
            )

        return data


class CustomUserSerializer(UserSerializer):
    """Сериализатор для работы с User."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def validate(self, data):
        if data.get('username') == 'me':
            raise ValidationError(
                "Имя пользователя 'me' зарезервировано в системе"
            )

    def get_is_subscribed(self, object):
        """Проверяет, подписан ли пользователь на автора."""

        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return object.author.filter(follower=request.user).exists()
        return False


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с Follow."""

    class Meta:
        model = Follow
        fields = ('author', 'follower')
        validators = (
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('author', 'follower'),
                message='Подписка на автора уже оформлена'
            ),
        )

    def validate(self, data):
        """Проверка на подписку на самого себя."""

        author = data.get('author')
        follower = data.get('follower')

        if follower == author:
            raise ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data


class FollowingStatusSerializer(CustomUserSerializer):
    """Сериализатор для вывода информации о подписках."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed'
        )

        # добавить 'recipes', 'recipes_count' и методы их получения
