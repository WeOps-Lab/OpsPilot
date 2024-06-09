from rest_framework import routers

from apps.model_provider_mgmt.views.embed_view import EmbedViewSet
from apps.model_provider_mgmt.views.rerank_view import RerankViewSet

router = routers.DefaultRouter()
router.register(r"api/embed", EmbedViewSet, basename="embed")
router.register(r"api/rerank", RerankViewSet, basename="rerank")
urlpatterns = router.urls
