from aiohttp.web_fileresponse import FileResponse
from apps.contentpack_mgmt.models import RasaModel
from apps.contentpack_mgmt.serializers import RasaModelSerializer
from django_minio_backend import MinioBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ModelViewSet


class RasaModelViewSet(ModelViewSet):
    serializer_class = RasaModelSerializer

    def get_queryset(self):
        queryset = RasaModel.objects.all()
        bot_id = self.request.query_params.get("bot_id", None)
        if bot_id is not None:
            queryset = queryset.filter(bot__id=bot_id)
        return queryset
