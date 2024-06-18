from rest_framework.viewsets import ModelViewSet

from apps.bot_mgmt.models import RasaModel
from apps.contentpack_mgmt.serializers import RasaModelSerializer


class RasaModelViewSet(ModelViewSet):
    serializer_class = RasaModelSerializer

    def get_queryset(self):
        queryset = RasaModel.objects.all()
        bot_id = self.request.query_params.get("bot_id", None)
        if bot_id is not None:
            queryset = queryset.filter(bot__id=bot_id)
        return queryset
