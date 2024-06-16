from rest_framework import viewsets, filters, pagination
from django_filters.rest_framework import DjangoFilterBackend
from apps.channel_mgmt.models import Channel
from apps.channel_mgmt.serializers import ChannelSerializer


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['channel_type', 'name']
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return Channel.objects.filter(owner=user)
