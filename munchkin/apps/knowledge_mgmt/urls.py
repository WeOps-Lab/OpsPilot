from rest_framework import routers

from apps.knowledge_mgmt.views.knowledge_search_viewset import KnowledgeSearchViewSet

router = routers.DefaultRouter()
router.register(r"api/knowledge_search", KnowledgeSearchViewSet, basename="knowledge_search")
urlpatterns = router.urls

urlpatterns += [
]
