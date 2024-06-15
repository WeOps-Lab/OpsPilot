from django.contrib.auth.models import User
from django.core.management import BaseCommand

from apps.contentpack_mgmt.services.contentpack_init_service import ContentPackInitService


class Command(BaseCommand):
    help = "初始化"

    def handle(self, *args, **options):
        admin_user = User.objects.get(username='admin')
        ContentPackInitService(owner=admin_user).init()
