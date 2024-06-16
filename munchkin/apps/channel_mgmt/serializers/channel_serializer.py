from apps.channel_mgmt.models import Channel
from rest_framework import serializers


class ChannelSerializer(serializers.ModelSerializer):
    channel_config = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = ['id', 'name', 'channel_type', 'channel_config']

    def get_channel_config(self, obj):
        return str(obj.channel_config)
