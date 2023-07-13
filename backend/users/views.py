from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from djoser.views import UserViewSet
from users.models import User
from rest_framework import permissions, status
from rest_framework.response import Response
from users.serializers import (
    CustomUserSerializer, FollowSerializer
)


from api.permissions import IsAnonymous, IsAuthenticated


class CustomUserViewSet(UserViewSet):
    """Вьюсет создания пользователя."""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer

    permission_classes = ((IsAnonymous | IsAuthenticated),)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
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
