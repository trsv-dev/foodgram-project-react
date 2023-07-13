from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import IsAnonymous, IsAuthenticated
from users.models import User, Follow
from users.serializers import (
    CustomUserSerializer, FollowSerializer, FollowingStatusSerializer
)


class CustomUserViewSet(UserViewSet):
    """Вьюсет создания пользователя."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    permission_classes = ((IsAnonymous | IsAuthenticated),)

    @action(
        detail=False, methods=['get', 'patch'], url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
        )
    def get_me(self, request):
        """Получение и редактирование информации о себе."""

        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                instance=request.user,
                data=request.data,
                partial=True,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(
            instance=request.user,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=['post', 'delete'], url_path='subscribe',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_subscribe(self, request, id=None):
        """Возможность подписываться и отписываться от автора."""

        user = request.user
        author = get_object_or_404(User, pk=id)

        if request.method == 'POST':
            serializer = FollowSerializer(
                data={'follower': user.id, 'author': author.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        subscription = get_object_or_404(Follow, follower=user, author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions',
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
