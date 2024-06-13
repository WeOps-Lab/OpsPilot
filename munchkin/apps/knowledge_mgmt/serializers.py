from rest_framework import serializers

from apps.knowledge_mgmt.models import ManualKnowledge


class ManualKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualKnowledge
        fields = '__all__'
