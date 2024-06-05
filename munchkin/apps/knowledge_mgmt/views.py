from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from apps.knowledge_mgmt.services.knowledge_service import KnowledgeService


class KnowledgeView(APIView):
    @swagger_auto_schema(
        operation_id="knowledge_search",
        operation_description="",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "knowledge_base_name": openapi.Schema(type=openapi.TYPE_STRING, description="知识库名称"),
                "keyword": openapi.Schema(type=openapi.TYPE_STRING, description="搜索内容"),
            },
            required=["knowledge_base_name", "keyword", ],
        ),
    )
    def post(self, request):
        knowledge_base_name = request.data.get('knowledge_base_name', '')
        keyword = request.data.get('keyword', '')

        service = KnowledgeService()
        result = service.knowledge_search(knowledge_base_name, keyword)

        return JsonResponse({
            "result": result
        })
