from apps.core.encoders import PrettyJSONEncoder
from apps.core.mixinx import EncryptableMixin
from django.db import models
from django.utils.functional import cached_property


class EmbedModelChoices(models.TextChoices):
    LANG_SERVE = "lang-serve", "LangServe"


class EmbedProvider(models.Model, EncryptableMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    embed_model_type = models.CharField(max_length=255, choices=EmbedModelChoices.choices, verbose_name="嵌入模型")
    embed_config = models.JSONField(
        verbose_name="嵌入配置",
        blank=True,
        null=True,
        encoder=PrettyJSONEncoder,
        default=dict,
    )
    enabled = models.BooleanField(default=True, verbose_name="是否启用")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Embed模型"
        verbose_name_plural = verbose_name
