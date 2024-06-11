from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action

from apps.model_provider_mgmt.models import RerankProvider
from apps.model_provider_mgmt.services.rerank_service import rerank_service


class RerankViewSet(viewsets.ViewSet):
    @action(methods=["post"], detail=False, url_path="rerank_sentences")
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "rerank_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "query": openapi.Schema(type=openapi.TYPE_STRING),
                "top_k": openapi.Schema(type=openapi.TYPE_INTEGER),
                "sentences": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
            },
        ),
    )
    def rerank_sentences(self, request):
        rerank_id = request.data.get("rerank_id")
        top_k = request.data.get("top_k")
        sentences = request.data.get("sentences")
        query = request.data.get("query")

        reranker = RerankProvider.objects.get(id=rerank_id)
        results = rerank_service.predict(reranker, top_k, sentences, query)

        return JsonResponse({
            "rerank_result": results
        })
