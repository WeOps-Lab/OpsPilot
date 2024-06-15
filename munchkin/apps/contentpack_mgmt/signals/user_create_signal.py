from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.contentpack_mgmt.services.contentpack_init_service import ContentPackInitService


@receiver(post_save, sender=User)
def user_create_signal(sender, instance, created, **kwargs):
    if created:
        service = ContentPackInitService(owner=instance)
        service.init()
