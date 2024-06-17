from apps.knowledge_mgmt.models import ManualKnowledge
from rest_framework import serializers


class ManualKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualKnowledge
        fields = "__all__"
