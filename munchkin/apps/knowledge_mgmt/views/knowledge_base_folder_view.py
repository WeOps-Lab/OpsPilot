from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from apps.knowledge_mgmt.serializers.knowledge_base_folder_serializer import KnowledgeBaseFolderSerializer
from apps.knowledge_mgmt.tasks.embed_task import general_embed
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action


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
    @action(methods=["post"], detail=False, url_path="search")
    def train(self, request):
        data = request.data
        knowledgebase_folder_ids = data.get("knowledgebase_folder_ids")
        for knowledgebase_folder_id in knowledgebase_folder_ids:
            general_embed.delay(knowledgebase_folder_id)
        results = {"result": True, "data": "success"}
        return JsonResponse(results)
