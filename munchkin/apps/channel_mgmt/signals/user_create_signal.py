from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.channel_mgmt.services.channel_init_service import ChannelInitService


@receiver(post_save, sender=User)
def user_create_signal(sender, instance, created, **kwargs):
    if created:
        service = ChannelInitService(owner=instance)
        service.init()
