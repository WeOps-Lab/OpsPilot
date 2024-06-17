from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from rest_framework import serializers


class KnowledgeBaseFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeBaseFolder
        fields = "__all__"
