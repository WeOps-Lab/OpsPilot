from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from apps.knowledge_mgmt.serializers.knowledge_base_folder_serializer import KnowledgeBaseFolderSerializer


class KnowledgeBaseFolderViewSet(GuardianModelViewSet):
    serializer_class = KnowledgeBaseFolderSerializer
    queryset = KnowledgeBaseFolder.objects.all()
    search_fields = ["name"]
