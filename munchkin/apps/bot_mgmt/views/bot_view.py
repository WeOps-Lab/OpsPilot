from rest_framework.viewsets import ModelViewSet

from apps.bot_mgmt.models import Bot
from apps.bot_mgmt.serializers import BotSerializer


class BotViewSet(ModelViewSet):
    serializer_class = BotSerializer
    queryset = Bot.objects.all()
