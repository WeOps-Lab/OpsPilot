from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.model_provider_mgmt.models import EmbedProvider
from apps.model_provider_mgmt.serializers.embed_serializer import EmbedProviderSerializer
from apps.model_provider_mgmt.services.embedding_service import emdedding_service
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action


class EmbedProviderViewSet(GuardianModelViewSet):
    serializer_class = EmbedProviderSerializer
    queryset = EmbedProvider.objects.all()
    search_fields = ["name", "embed_model"]
    superuser_only = True


class EmbedViewSet(viewsets.ViewSet):
    @action(methods=["post"], detail=False, url_path="embed_content")
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "embed_model_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "content": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    def embed_content(self, request):
        embed_model_id = request.data.get("embed_model_id")
        content = request.data.get("content")
        embed_provider = EmbedProvider.objects.get(id=embed_model_id)
        embedding = emdedding_service.embed_content(embed_provider, content)
        return JsonResponse({"embedding": embedding})
