from django.contrib.auth.models import User

from apps.bot_mgmt.models import Bot
from apps.bot_mgmt.services.bot_init_service import BotInitService
from apps.channel_mgmt.models import CHANNEL_CHOICES, Channel
from apps.contentpack_mgmt.models import RasaModel
from apps.model_provider_mgmt.models import LLMSkill
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "初始化机器人"

    def handle(self, *args, **options):
        admin_user = User.objects.get(username='admin')
        BotInitService(owner=admin_user).init()
