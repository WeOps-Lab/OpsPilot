from rest_framework import routers

from apps.model_provider_mgmt.views.embed_view import EmbedViewSet, EmbedProviderViewSet
from apps.model_provider_mgmt.views.llm_view import LLMViewSet

router = routers.DefaultRouter()
router.register(r"api/embed", EmbedViewSet, basename="embed")
router.register(r"api/embed_provider", EmbedProviderViewSet, basename="embed_provider")
router.register(r"api/llm", LLMViewSet, basename="llm")
urlpatterns = router.urls
