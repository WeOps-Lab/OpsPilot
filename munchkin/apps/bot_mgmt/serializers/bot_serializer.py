from apps.bot_mgmt.models import Bot
from apps.channel_mgmt.serializers import ChannelDecryptedSerializer
from rest_framework import serializers


class BotSerializer(serializers.ModelSerializer):
    channels = ChannelDecryptedSerializer(many=True)

    class Meta:
        model = Bot
        fields = "__all__"
