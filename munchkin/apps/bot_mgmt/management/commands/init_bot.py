from django.contrib.auth.models import User

from apps.bot_mgmt.services.bot_init_service import BotInitService
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "初始化机器人"

    def handle(self, *args, **options):
        admin_user = User.objects.get(username='admin')
        BotInitService(owner=admin_user).init()
