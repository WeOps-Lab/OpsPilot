from django.contrib.auth.models import User

from django.core.management import BaseCommand
from apps.model_provider_mgmt.services.model_provider_init_service import ModelProviderInitService


class Command(BaseCommand):
    help = "初始化模型数据"

    def handle(self, *args, **options):
        admin_user = User.objects.get(username='admin')
        ModelProviderInitService(owner=admin_user).init()
