import hashlib

from apps.bot_mgmt.models import Bot
from apps.contentpack_mgmt.models import RasaModel
from django.http import FileResponse
from django_minio_backend import MinioBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


class ModelDownloadView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Download a RasaModel file",
        responses={200: openapi.Response(description="File downloaded successfully")},
    )
    def get(self, request, format=None):
        try:
            bot_id = request.query_params.get("bot_id")
            rasa_model = Bot.objects.filter(id=bot_id).first().rasa_model
        except RasaModel.DoesNotExist:
            raise NotFound("RasaModel with given id not found")

        storage = MinioBackend(bucket_name="munchkin-private")
        file = storage.open(rasa_model.model_file.name, "rb")

        # Calculate ETag
        data = file.read()
        etag = hashlib.md5(data).hexdigest()

        # Reset file pointer to start
        file.seek(0)

        response = FileResponse(file)
        response["ETag"] = etag

        return response
