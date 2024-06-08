from django.db import models
from django.utils.functional import cached_property

from apps.core.encoders import PrettyJSONEncoder
from apps.core.mixinx import EncryptableMixin
from apps.knowledge_mgmt.models import KnowledgeBaseFolder


class LLMModelChoices(models.TextChoices):
    CHAT_GPT = 'chat-gpt', 'ChatGPT'


class LLMModel(models.Model, EncryptableMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    llm_model = models.CharField(max_length=255, choices=LLMModelChoices.choices, verbose_name='LLM模型')
    llm_config = models.JSONField(verbose_name='LLM配置', blank=True, null=True, encoder=PrettyJSONEncoder,
                                  default=dict)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.llm_model == LLMModelChoices.CHAT_GPT:
            self.encrypt_field('openai_api_key', self.llm_config)
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_llm_config(self):
        llm_config_decrypted = self.llm_config.copy()

        if self.llm_model == LLMModelChoices.CHAT_GPT:
            self.decrypt_field('openai_api_key', llm_config_decrypted)
        return llm_config_decrypted

    class Meta:
        verbose_name = "LLM模型"
        verbose_name_plural = verbose_name


class LLMSkill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    llm_model = models.ForeignKey(LLMModel, on_delete=models.CASCADE, verbose_name='LLM模型', blank=True, null=True)
    skill_id = models.CharField(max_length=255, verbose_name='技能ID', blank=True, null=True)
    skill_prompt = models.TextField(blank=True, null=True, verbose_name='技能提示词')

    enable_conversation_history = models.BooleanField(default=False, verbose_name='启用对话历史')
    conversation_window_size = models.IntegerField(default=10, verbose_name='对话窗口大小')

    enable_rag = models.BooleanField(default=False, verbose_name='启用RAG')
    knowledge_base_folders = models.ManyToManyField(KnowledgeBaseFolder, blank=True, verbose_name='知识库')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "LLM技能管理"
        verbose_name_plural = verbose_name


class RerankModelChoices(models.TextChoices):
    BCE = 'bce', 'BCE'


class RerankProvider(models.Model, EncryptableMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    rerank_model = models.CharField(max_length=255, choices=RerankModelChoices.choices, verbose_name='Rerank模型')
    rerank_config = models.JSONField(verbose_name='Rerank配置', blank=True, null=True, encoder=PrettyJSONEncoder,
                                     default=dict)
    enabled = models.BooleanField(default=True, verbose_name='是否启用')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_rerank_config_config(self):
        rerank_config_decrypted = self.rerank_config.copy()
        return rerank_config_decrypted

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rerank模型"
        verbose_name_plural = verbose_name


class EmbedModelChoices(models.TextChoices):
    FASTEMBED = 'fastembed', 'FastEmbed'
    OPENAI = 'openai', 'OpenAI'
    BCEEMBEDDING = 'bceembedding', 'BCEEmbedding'


class EmbedProvider(models.Model, EncryptableMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    embed_model = models.CharField(max_length=255, choices=EmbedModelChoices.choices, verbose_name='嵌入模型')
    embed_config = models.JSONField(verbose_name='嵌入配置', blank=True, null=True, encoder=PrettyJSONEncoder,
                                    default=dict)
    enabled = models.BooleanField(default=True, verbose_name='是否启用')

    def save(self, *args, **kwargs):
        if self.embed_model == EmbedModelChoices.OPENAI:
            self.encrypt_field('openai_api_key', self.embed_config)
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_embed_config(self):
        embed_config_decrypted = self.embed_config.copy()
        if self.embed_model == EmbedModelChoices.OPENAI:
            self.decrypt_field('openai_api_key', embed_config_decrypted)
        return embed_config_decrypted

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Embed模型"
        verbose_name_plural = verbose_name
