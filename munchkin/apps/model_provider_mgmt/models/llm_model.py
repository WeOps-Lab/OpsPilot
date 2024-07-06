from apps.core.encoders import PrettyJSONEncoder
from apps.core.mixinx import EncryptableMixin
from django.db import models
from django.utils.functional import cached_property


class LLMModelChoices(models.TextChoices):
    CHAT_GPT = "chat-gpt", "ChatGPT"
    ZHIPU = "zhipu", "智谱AI"


class LLMModel(models.Model, EncryptableMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    llm_model_type = models.CharField(max_length=255, choices=LLMModelChoices.choices, verbose_name="LLM模型类型")
    llm_config = models.JSONField(
        verbose_name="LLM配置",
        blank=True,
        null=True,
        encoder=PrettyJSONEncoder,
        default=dict,
    )
    enabled = models.BooleanField(default=True, verbose_name="启用")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.llm_model_type == LLMModelChoices.CHAT_GPT:
            self.encrypt_field("openai_api_key", self.llm_config)
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_llm_config(self):
        llm_config_decrypted = self.llm_config.copy()

        if self.llm_model_type == LLMModelChoices.CHAT_GPT:
            self.decrypt_field("openai_api_key", llm_config_decrypted)
        return llm_config_decrypted

    class Meta:
        verbose_name = "LLM模型"
        verbose_name_plural = verbose_name
