import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.bot_mgmt.models import Bot
from loguru import logger


@receiver(post_save, sender=Bot)
def restart_service_after_save(sender, **kwargs):
    try:
        logger.info('重启conversation服务')
        os.system("supervisorctl restart conversation")
    except Exception:
        pass


@receiver(post_delete, sender=Bot)
def restart_service_after_delete(sender, **kwargs):
    try:
        logger.info('重启conversation服务')
        os.system("supervisorctl restart conversation")
    except Exception:
        pass
