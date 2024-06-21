from apps.core.viewsets.guardian_model_viewset import GuardianModelViewSet
from apps.knowledge_mgmt.models import ManualKnowledge
from apps.knowledge_mgmt.serializers.manual_knowledge_serializer import ManualKnowledgeSerializer


class ManualKnowledgeViewSet(GuardianModelViewSet):
    serializer_class = ManualKnowledgeSerializer
    queryset = ManualKnowledge.objects.all()
    search_fields = [
        "title",
        "content",
        "custom_metadata",
    ]
