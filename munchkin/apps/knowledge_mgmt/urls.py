from apps.knowledge_mgmt.views.file_knowledge_view import FileKnowledgeViewSet
from apps.knowledge_mgmt.views.knowledge_base_folder_view import KnowledgeBaseFolderViewSet
from apps.knowledge_mgmt.views.knowledge_search_viewset import KnowledgeSearchViewSet
from apps.knowledge_mgmt.views.manual_knowledge_view import ManualKnowledgeViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"api/manual_knowledge", ManualKnowledgeViewSet)
router.register(r"api/file_knowledge", FileKnowledgeViewSet)
router.register(r"api/knowledge", KnowledgeSearchViewSet, basename="knowledge_search")
router.register(r"api/knowledge_base_folder", KnowledgeBaseFolderViewSet, basename="knowledge_base_folder")
urlpatterns = router.urls

urlpatterns += []
