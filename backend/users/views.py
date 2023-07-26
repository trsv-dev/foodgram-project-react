from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAnonymous, IsAuthenticated
from api.serializers import (
    CustomUserSerializer, FollowSerializer, FollowingStatusSerializer
)
from users.models import User, Follow


class CustomUserViewSet(UserViewSet):
    """Вьюсет создания пользователя."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = ((IsAnonymous | IsAuthenticated),)

    @action(
        detail=True, methods=['POST', 'DELETE'], url_path='subscribe',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_subscribe(self, request, id=None):
        """Возможность подписываться и отписываться от автора."""

        follower = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'DELETE':
            get_object_or_404(
                Follow, follower=request.user, author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

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

        serializer = CustomUserSerializer(
            instance=request.user,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
