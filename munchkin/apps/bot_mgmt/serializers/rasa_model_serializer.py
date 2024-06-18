from rest_framework import serializers

from apps.bot_mgmt.models import RasaModel


class RasaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RasaModel
        fields = "__all__"
