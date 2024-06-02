from rest_framework import serializers

from apps.channel_mgmt.models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = '__all__'
