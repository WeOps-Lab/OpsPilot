from django.contrib.auth.models import User
from django.core.management import BaseCommand

from apps.channel_mgmt.services.channel_init_service import ChannelInitService


class Command(BaseCommand):
    help = "初始化消息通道"

    def handle(self, *args, **options):
        admin_user = User.objects.get(username='admin')
        ChannelInitService(owner=admin_user).init()
