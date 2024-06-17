from apps.knowledge_mgmt.models import ManualKnowledge
from apps.knowledge_mgmt.serializers.manual_knowledge_serializer import ManualKnowledgeSerializer
from rest_framework.viewsets import ModelViewSet


class ManualKnowledgeViewSet(ModelViewSet):
    serializer_class = ManualKnowledgeSerializer
    queryset = ManualKnowledge.objects.all()
