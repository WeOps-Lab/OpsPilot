from apps.contentpack_mgmt.models import RasaModel
from django.http import FileResponse
from django_minio_backend import MinioBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView


class TrainDataDownloadView(APIView):
    @swagger_auto_schema(
        operation_description="Download a RasaModel file",
        responses={200: openapi.Response(description="File downloaded successfully")},
    )
    def get(self, request, format=None):
        model_id = request.query_params.get("model_id")
        rasa_model = RasaModel.objects.get(id=model_id)
        storage = MinioBackend(bucket_name="munchkin-private")
        file = storage.open(rasa_model.train_data_file.name, "rb")
        response = FileResponse(file)

        return response
