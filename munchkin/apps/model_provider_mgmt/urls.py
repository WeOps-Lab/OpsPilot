from apps.model_provider_mgmt.views.embed_view import EmbedViewSet
from apps.model_provider_mgmt.views.llm_view import LLMViewSet
from apps.model_provider_mgmt.views.rerank_view import RerankViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"api/embed", EmbedViewSet, basename="embed")
router.register(r"api/rerank", RerankViewSet, basename="rerank")
router.register(r"api/llm", LLMViewSet, basename="llm")
urlpatterns = router.urls
