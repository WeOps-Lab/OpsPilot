from apps.channel_mgmt.models import Channel
from rest_framework import serializers


class ChannelDecryptedSerializer(serializers.ModelSerializer):
    decrypted_channel_config = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = "__all__"

    def get_decrypted_channel_config(self, obj):
        return obj.decrypted_channel_config

