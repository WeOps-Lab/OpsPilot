from django_yaml_field.fields import YAMLField

from apps.core.models.maintainer_info import MaintainerInfo
from django.db import models
from django.utils.functional import cached_property


class KNOWLEDGE_INTEGRATION_CHOICES(models.TextChoices):
    WEOPS = ("weops", "WeOps")
    PLAYWRIGHT = ("playwright", "Playwright")
    WEB_SCRAPY = ("simple_web_scrapy", "网站爬虫")


class KnowledgeIntegration(MaintainerInfo):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name="集成名称")
    integration_config = YAMLField(verbose_name="集成配置", blank=True, null=True)
    integration = models.CharField(max_length=100, choices=KNOWLEDGE_INTEGRATION_CHOICES.choices, verbose_name="集成")

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
        verbose_name = "知识集成"
        verbose_name_plural = verbose_name
