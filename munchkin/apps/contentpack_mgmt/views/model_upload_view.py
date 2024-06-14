import os

from apps.contentpack_mgmt.models import RasaModel
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ModelUploadView(APIView):
    @swagger_auto_schema(
        operation_description="Upload a RasaModel file",
        responses={201: openapi.Response(description="File uploaded successfully")},
    )
    def post(self, request, format=None):
        file_obj = request.FILES.get("file")
        model_id = request.query_params.get("model_id")

        if not file_obj or not isinstance(file_obj, InMemoryUploadedFile):
            return Response(
                {"detail": "No file was provided or the provided file is invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not model_id:
            return Response(
                {"detail": "No bot_id was provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        rasa_model = RasaModel.objects.get(id=model_id)
        rasa_model.model_file = File(file_obj, name=os.path.basename(file_obj.name))
        rasa_model.save()

        return Response({"model_id": rasa_model.id}, status=status.HTTP_201_CREATED)
