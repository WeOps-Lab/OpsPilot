from rest_framework.viewsets import ModelViewSet

from apps.knowledge_mgmt.models import ManualKnowledge
from apps.knowledge_mgmt.serializers import ManualKnowledgeSerializer


class ManualKnowledgeSet(ModelViewSet):
    serializer_class = ManualKnowledgeSerializer
    queryset = ManualKnowledge.objects.all()
