from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.knowledge_mgmt.models import KnowledgeBaseFolder, ManualKnowledge
from apps.knowledge_mgmt.serializers.manual_knowledge_serializer import ManualKnowledgeSerializer
from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action


class ManualKnowledgeViewSet(GuardianModelViewSet):
    serializer_class = ManualKnowledgeSerializer
    queryset = ManualKnowledge.objects.all()
    search_fields = [
        "title",
        "content",
        "custom_metadata",
    ]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "knowledgebase_folder_ids": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                ),
                "query": openapi.Schema(type=openapi.TYPE_STRING),
                "metadata": openapi.Schema(type=openapi.TYPE_OBJECT),
                "score_threshold": openapi.Schema(type=openapi.TYPE_NUMBER),
                "docs_return_num": openapi.Schema(type=openapi.TYPE_NUMBER),
            },
        ),
    )
    @action(methods=["post"], detail=False, url_path="search")
    def search(self, request):
        data = request.data
        knowledgebase_folder_ids = data.get("knowledgebase_folder_ids")
        query = data.get("query")
        metadata = data.get("metadata", {})
        score_threshold = data.get("score_threshold", 0)
        docs_return_num = data.get("docs_return_num", 10)
        if query:
            service = KnowledgeSearchService()
            knowledgebase_folders = KnowledgeBaseFolder.objects.filter(id__in=knowledgebase_folder_ids)
            docs = service.search(knowledgebase_folders, query, metadata, score_threshold)
            doc_ids = [doc["knowledge_id"] for doc in docs]
            manual_knowledge = ManualKnowledge.objects.filter(id__in=set(doc_ids))[:docs_return_num]
        else:
            manual_knowledge = ManualKnowledge.objects.all()[:docs_return_num]

        serializer = ManualKnowledgeSerializer(manual_knowledge, many=True)
        results = {"result": True, "data": {"count": len(manual_knowledge), "items": serializer.data}}
        return JsonResponse(results)
