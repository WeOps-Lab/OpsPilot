import os

from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import FileResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from django_minio_backend import MinioBackend
from rest_framework.viewsets import ModelViewSet

from apps.bot_mgmt.models import Bot
from apps.contentpack_mgmt.models import RasaModel
import hashlib


class RasaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RasaModel
        fields = '__all__'


class RasaModelViewSet(ModelViewSet):
    serializer_class = RasaModelSerializer

    def get_queryset(self):
        queryset = RasaModel.objects.all()
        bot_id = self.request.query_params.get('bot_id', None)
        if bot_id is not None:
            queryset = queryset.filter(bot__id=bot_id)
        return queryset


class TrainDataDownloadView(APIView):

    @swagger_auto_schema(
        operation_description="Download a RasaModel file",
        responses={200: openapi.Response(description="File downloaded successfully")}
    )
    def get(self, request, format=None):
        try:
            bot_id = request.query_params.get('bot_id')
            bot = Bot.objects.filter(id=bot_id).first()
        except Bot.DoesNotExist:
            raise NotFound("Bot with given id not found")

        storage = MinioBackend(bucket_name='munchkin-private')
        file = storage.open(bot.rasa_model.train_data_file.name, 'rb')

        # Calculate ETag
        data = file.read()

        # Reset file pointer to start
        file.seek(0)

        response = FileResponse(file)

        return response


class ModelUploadView(APIView):

    @swagger_auto_schema(
        operation_description="Upload a RasaModel file",
        responses={201: openapi.Response(description="File uploaded successfully")}
    )
    def post(self, request, format=None):
        file_obj = request.FILES.get('file')
        bot_id = request.query_params.get('bot_id')

        if not file_obj or not isinstance(file_obj, InMemoryUploadedFile):
            return Response({"detail": "No file was provided or the provided file is invalid."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not bot_id:
            return Response({"detail": "No bot_id was provided."},
                            status=status.HTTP_400_BAD_REQUEST)

        rasa_model = Bot.objects.filter(id=bot_id).first().rasa_model
        rasa_model.model_file = File(file_obj, name=os.path.basename(file_obj.name))
        rasa_model.save()

        return Response({"model_id": rasa_model.id}, status=status.HTTP_201_CREATED)


class ModelDownloadView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Download a RasaModel file",
        responses={200: openapi.Response(description="File downloaded successfully")}
    )
    def get(self, request, format=None):
        try:
            bot_id = request.query_params.get('bot_id')
            rasa_model = Bot.objects.filter(id=bot_id).first().rasa_model
        except RasaModel.DoesNotExist:
            raise NotFound("RasaModel with given id not found")

        storage = MinioBackend(bucket_name='munchkin-private')
        file = storage.open(rasa_model.model_file.name, 'rb')

        # Calculate ETag
        data = file.read()
        etag = hashlib.md5(data).hexdigest()

        # Reset file pointer to start
        file.seek(0)

        response = FileResponse(file)
        response["ETag"] = etag

        return response
