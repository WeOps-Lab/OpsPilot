from apps.core.encoders import PrettyJSONEncoder
from apps.core.mixinx import EncryptableMixin
from django.db import models
from django.utils.functional import cached_property


class EmbedModelChoices(models.TextChoices):
    FASTEMBED = "fastembed", "FastEmbed"
    OPENAI = "openai", "OpenAI"
    BCEEMBEDDING = "bceembedding", "BCEEmbedding"


class EmbedProvider(models.Model, EncryptableMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    embed_model = models.CharField(max_length=255, choices=EmbedModelChoices.choices, verbose_name="嵌入模型")
    embed_config = models.JSONField(
        verbose_name="嵌入配置",
        blank=True,
        null=True,
        encoder=PrettyJSONEncoder,
        default=dict,
    )
    enabled = models.BooleanField(default=True, verbose_name="是否启用")

    def save(self, *args, **kwargs):
        if self.embed_model == EmbedModelChoices.OPENAI:
            self.encrypt_field("openai_api_key", self.embed_config)
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_embed_config(self):
        embed_config_decrypted = self.embed_config.copy()
        if self.embed_model == EmbedModelChoices.OPENAI:
            self.decrypt_field("openai_api_key", embed_config_decrypted)
        return embed_config_decrypted

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Embed模型"
        verbose_name_plural = verbose_name
