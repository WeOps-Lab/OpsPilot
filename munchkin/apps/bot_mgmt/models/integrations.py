from apps.core.encoders import PrettyJSONEncoder
from apps.core.mixinx import EncryptableMixin
from apps.core.models.maintainer_info import MaintainerInfo
from django.db import models
from django.utils.functional import cached_property


class IntegrationChoices(models.TextChoices):
    SALT = "salt", "SALT"
    WEOPS = "weops", "WeOps"
    JENKINS = "jenkins", "Jenkins"


class Integrations(MaintainerInfo, EncryptableMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="名称")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    integration_type = models.CharField(max_length=255, verbose_name="类型", choices=IntegrationChoices.choices)
    config = models.JSONField(verbose_name="配置", default=dict,
                              null=True,
                              encoder=PrettyJSONEncoder, )
    bot_id = models.ForeignKey("bot_mgmt.Bot", on_delete=models.CASCADE, verbose_name="机器人", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.config is not None:
            if "password" in self.config:
                self.encrypt_field(
                    "password", self.config
                )
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_config(self):
        decrypted_config = self.config.copy()
        if "password" in self.config:
            self.decrypt_field("password", decrypted_config)
        return decrypted_config

    class Meta:
        verbose_name = "集成"
        verbose_name_plural = verbose_name
