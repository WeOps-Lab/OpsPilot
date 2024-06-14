from apps.contentpack_mgmt.models import RasaModel
from rest_framework import serializers


class RasaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RasaModel
        fields = "__all__"
