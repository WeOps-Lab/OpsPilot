from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from apps.knowledge_mgmt.serializers.knowledge_base_folder_serializer import KnowledgeBaseFolderSerializer
from rest_framework.viewsets import ModelViewSet


class KnowledgeBaseFolderViewSet(ModelViewSet):
    serializer_class = KnowledgeBaseFolderSerializer
    queryset = KnowledgeBaseFolder.objects.all()
    search_fields = ["name"]
