from apps.core.mixinx import EncryptableMixin
from apps.core.models.maintainer_info import MaintainerInfo
from django.db import models
from django.utils.functional import cached_property
from django_yaml_field import YAMLField


class INTEGRATION_CHOICES(models.TextChoices):
    JENKINS = ("jenkins", "Jenkins")


class Integration(MaintainerInfo, EncryptableMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="名称")
    integration = models.CharField(max_length=100, choices=INTEGRATION_CHOICES.choices, verbose_name="集成")
    integration_config = YAMLField(verbose_name="集成配置", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.integration_config is not None:
            self.encrypt_field("password", self.integration_config)
            self.encrypt_field("token", self.integration_config)

        super().save(*args, **kwargs)

    @cached_property
    def decrypted_integration_config(self):
        decrypted_config = self.integration_config.copy()
        self.decrypt_field("password", decrypted_config)
        self.decrypt_field("token", decrypted_config)

        return decrypted_config

    class Meta:
        verbose_name = "集成"
        verbose_name_plural = verbose_name
