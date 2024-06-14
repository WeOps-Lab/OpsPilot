from django.db.models import Q
from rest_framework import mixins, viewsets


class OwnerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    def get_queryset(self):
        """
        This view should return a list of all the records
        for the currently authenticated user.
        """
        user = self.request.user
        return self.queryset.filter(Q(owner=user) | Q(is_public=True))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
