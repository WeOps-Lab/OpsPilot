import os
import zipfile

from django.core.files.base import ContentFile
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from loguru import logger
from tqdm.std import tqdm

from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.knowledge_mgmt.models import KnowledgeBaseFolder, FileKnowledge
from apps.knowledge_mgmt.serializers.knowledge_base_folder_serializer import KnowledgeBaseFolderSerializer
from apps.knowledge_mgmt.tasks.embed_task import general_embed


class KnowledgeBaseFolderViewSet(GuardianModelViewSet):
    serializer_class = KnowledgeBaseFolderSerializer
    queryset = KnowledgeBaseFolder.objects.all()
    search_fields = ["name"]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "knowledgebase_folder_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                ),
            },
        ),
    )
    @action(methods=["post"], detail=False, url_path="train")
    def train(self, request):
        data = request.data
        knowledgebase_folder_ids = data.get("knowledgebase_folder_ids")
        for knowledgebase_folder_id in knowledgebase_folder_ids:
            general_embed.delay(knowledgebase_folder_id)
        results = {"result": True, "data": "success"}
        return JsonResponse(results)

    @swagger_auto_schema(method='post',
                         operation_description="Upload a zip file and store its contents in the database",
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'file': openapi.Schema(type=openapi.TYPE_FILE,
                                                        description='The zip file to upload')
                             }),
                         responses={201: "Upload successful", 400: "Invalid file or missing field"})
    @action(detail=True, methods=['post'], url_path='import_file_knowledges')
    def import_file_knowledges(self, request, pk=None):
        try:
            knowledge_base_folder = KnowledgeBaseFolder.objects.get(id=pk)
            file = request.FILES['file']
            if not zipfile.is_zipfile(file):
                return JsonResponse({'error': 'Invalid zip file'}, status=status.HTTP_400_BAD_REQUEST)

            with zipfile.ZipFile(file) as zf:
                for name in tqdm(zf.namelist()):
                    if name.endswith('/') or name.startswith('__MACOSX'):
                        continue

                    title = os.path.basename(name.encode('cp437').decode('utf-8')).strip()
                    if not title:
                        logger.warning(f'File with empty title found: {name}')
                        continue

                    content = zf.read(name)
                    if not content:
                        logger.warning(f'Empty content for file: {title}')
                        continue

                    logger.info(f'Reading file: [{title}]')
                    content_file = ContentFile(content, name=title)

                    FileKnowledge.objects.get_or_create(title=title,
                                                        file=content_file,
                                                        knowledge_base_folder=knowledge_base_folder)

            return JsonResponse({'message': 'Upload successful'}, status=status.HTTP_201_CREATED)

        except KnowledgeBaseFolder.DoesNotExist:
            logger.error(f'Knowledge base folder with id {pk} does not exist')
            return JsonResponse({'error': 'Knowledge base folder not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Failed to import file: {e}')
            return JsonResponse({'error': 'File import failed'}, status=status.HTTP_400_BAD_REQUEST)
