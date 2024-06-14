from apps.knowledge_mgmt.views.knowledge_search_viewset import KnowledgeSearchViewSet
from apps.knowledge_mgmt.views.manual_knowledge_view import ManualKnowledgeSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"api/manual_knowledge", ManualKnowledgeSet)
router.register(r"api/knowledge_search", KnowledgeSearchViewSet, basename="knowledge_search")
urlpatterns = router.urls

urlpatterns += []
