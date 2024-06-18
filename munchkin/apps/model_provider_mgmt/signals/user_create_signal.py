from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.model_provider_mgmt.services.model_provider_init_service import ModelProviderInitService


@receiver(post_save, sender=User)
def user_create_signal(sender, instance, created, **kwargs):
    if created and instance.username != 'AnonymousUser':
        service = ModelProviderInitService(owner=instance)
        service.init()
