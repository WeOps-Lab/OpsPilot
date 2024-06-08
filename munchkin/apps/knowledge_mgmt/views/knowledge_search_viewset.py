from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from apps.knowledge_mgmt.services.knowledge_search_service import KnowledgeSearchService


class KnowledgeSearchViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "knowledgebase_folder_ids": openapi.Schema(type=openapi.TYPE_ARRAY,
                                                           items=openapi.Schema(type=openapi.TYPE_INTEGER)),
                "query": openapi.Schema(type=openapi.TYPE_STRING),
                "metadata": openapi.Schema(type=openapi.TYPE_OBJECT),
            },
        ),
    )
    @action(methods=["post"], detail=False, url_path="search")
    def search(self, request):
        data = request.data
        knowledgebase_folder_ids = data.get("knowledgebase_folder_ids")
        query = data.get("query")
        metadata = data.get("metadata", {})

        service = KnowledgeSearchService()
        knowledgebase_folders = KnowledgeBaseFolder.objects.filter(id__in=knowledgebase_folder_ids)
        docs = service.search(knowledgebase_folders, query, metadata)
        results = {
            'chunks': []
        }
        for doc in docs:
            results['chunks'].append({
                "page_content": doc.page_content,
            })
        return JsonResponse(results)
