from apps.knowledge_mgmt.models import FileKnowledge
from rest_framework import serializers


class FileKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileKnowledge
        fields = "__all__"
