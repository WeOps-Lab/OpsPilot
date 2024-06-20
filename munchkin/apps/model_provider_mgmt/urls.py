from rest_framework import routers

from apps.model_provider_mgmt.views.llm_view import LLMViewSet

router = routers.DefaultRouter()
router.register(r"api/llm", LLMViewSet, basename="llm")
urlpatterns = router.urls
