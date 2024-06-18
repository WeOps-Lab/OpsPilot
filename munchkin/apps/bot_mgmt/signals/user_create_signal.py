from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.bot_mgmt.services.bot_init_service import BotInitService


@receiver(post_save, sender=User)
def user_create_signal(sender, instance, created, **kwargs):
    if created and instance.username != 'AnonymousUser':
        service = BotInitService(owner=instance)
        service.init()
