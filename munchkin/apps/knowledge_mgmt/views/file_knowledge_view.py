from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.knowledge_mgmt.models import FileKnowledge
from apps.knowledge_mgmt.serializers.file_knowledge_serializer import FileKnowledgeSerializer


class FileKnowledgeViewSet(GuardianModelViewSet):
    serializer_class = FileKnowledgeSerializer
    queryset = FileKnowledge.objects.all()
    search_fields = ["title"]

    def get_queryset(self):
        queryset = FileKnowledge.objects.all()
        title_exclude = self.request.GET.get("title_exclude", "")
        knowledge_base_folder_ids = self.request.GET.get("knowledge_base_folder_ids", [])
        if title_exclude:
            queryset = queryset.exclude(title__contains=title_exclude)
        if knowledge_base_folder_ids:
            if isinstance(knowledge_base_folder_ids, str):
                knowledge_base_folder_ids = [knowledge_base_folder_ids]
            queryset = queryset.filter(knowledge_base_folder__in=knowledge_base_folder_ids)

        return queryset
