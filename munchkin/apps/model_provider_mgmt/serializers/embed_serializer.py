from apps.model_provider_mgmt.models import EmbedProvider
from rest_framework import serializers


class EmbedProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmbedProvider
        fields = "__all__"
