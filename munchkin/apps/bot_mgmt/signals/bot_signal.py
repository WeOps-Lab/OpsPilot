import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.bot_mgmt.models import Bot
from loguru import logger
import time
import threading


def restart_service():
    try:
        time.sleep(10)
        logger.info('重启conversation服务')
        os.system("supervisorctl restart conversation")
    except Exception:
        pass


@receiver(post_save, sender=Bot)
def restart_service_after_save(sender, **kwargs):
    thread = threading.Thread(target=restart_service)
    thread.start()


@receiver(post_delete, sender=Bot)
def restart_service_after_delete(sender, **kwargs):
    thread = threading.Thread(target=restart_service)
    thread.start()
