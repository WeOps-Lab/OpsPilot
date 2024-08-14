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
        if title_exclude:
            queryset = queryset.exclude(title__contains=title_exclude)

        return queryset
