from langchain_core.documents import Document

from apps.model_provider_mgmt.models import RerankProvider
from apps.model_provider_mgmt.services.rerank_service import RerankService
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action


class RerankViewSet(viewsets.ViewSet):
    @action(methods=["post"], detail=False, url_path="rerank_sentences")
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "rerank_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "query": openapi.Schema(type=openapi.TYPE_STRING),
                "top_k": openapi.Schema(type=openapi.TYPE_INTEGER),
                "sentences": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                ),
            },
        ),
    )
    def rerank_sentences(self, request):
        rerank_id = request.data.get("rerank_id")
        top_k = request.data.get("top_k")
        sentences = request.data.get("sentences")
        query = request.data.get("query")

        reranker = RerankProvider.objects.get(id=rerank_id)

        rerank_service = RerankService()
        docs = []
        for sentence in sentences:
            docs.append(Document(page_content=sentence))
        results = rerank_service.execute(reranker, docs, query, top_k)
        response = []
        for result in results:
            response.append({
                'content': result.page_content,
                'relevance_score': result.metadata['relevance_score']
            })
        return JsonResponse({"rerank_result": response})
