from apps.knowledge_mgmt.models import ManualKnowledge
from apps.knowledge_mgmt.serializers import ManualKnowledgeSerializer
from rest_framework.viewsets import ModelViewSet


class ManualKnowledgeSet(ModelViewSet):
    serializer_class = ManualKnowledgeSerializer
    queryset = ManualKnowledge.objects.all()
