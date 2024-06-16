from apps.bot_mgmt.models import Bot
from rest_framework import serializers

from apps.channel_mgmt.serializers import ChannelSerializer


class BotSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True)

    class Meta:
        model = Bot
        fields = "__all__"
