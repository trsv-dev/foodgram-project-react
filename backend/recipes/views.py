from rest_framework import viewsets, permissions
from rest_framework.viewsets import ReadOnlyModelViewSet
from recipes.models import Tags
from recipes.serializers import TagsSerializer


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (permissions.AllowAny,)
