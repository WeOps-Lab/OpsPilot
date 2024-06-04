import base64

from django.db import models
from django.utils.functional import cached_property
from apps.core.encoders import PrettyJSONEncoder
from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from cryptography.fernet import Fernet

from munchkin.components.base import SECRET_KEY


class LLMModelChoices(models.TextChoices):
    CHAT_GPT = 'chat-gpt', 'ChatGPT'


class LLMModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    llm_model = models.CharField(max_length=255, choices=LLMModelChoices.choices, verbose_name='LLM模型')
    llm_config = models.JSONField(verbose_name='LLM配置', blank=True, null=True, encoder=PrettyJSONEncoder,
                                  default=dict)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        key = base64.urlsafe_b64encode(SECRET_KEY.encode()[:32])
        cipher_suite = Fernet(key)
        if self.llm_model == LLMModelChoices.CHAT_GPT:
            openai_api_key = self.llm_config.get('openai_api_key')
            if openai_api_key:
                try:
                    cipher_suite.decrypt(openai_api_key.encode())
                except Exception:
                    encrypted_key = cipher_suite.encrypt(openai_api_key.encode())
                    self.llm_config['openai_api_key'] = encrypted_key.decode()
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_llm_config(self):
        key = base64.urlsafe_b64encode(SECRET_KEY.encode()[:32])
        cipher_suite = Fernet(key)
        llm_config_decrypted = self.llm_config.copy()
        if self.llm_model == LLMModelChoices.CHAT_GPT:
            encrypted_openai_api_key = self.llm_config.get('openai_api_key')
            if encrypted_openai_api_key:
                try:
                    decrypted_key = cipher_suite.decrypt(encrypted_openai_api_key.encode())
                    llm_config_decrypted['openai_api_key'] = decrypted_key.decode()
                except Exception:
                    pass
        return llm_config_decrypted

    class Meta:
        verbose_name = "LLM模型"
        verbose_name_plural = verbose_name


class LLMSkill(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    llm_model = models.ForeignKey(LLMModel, on_delete=models.CASCADE, verbose_name='LLM模型', blank=True, null=True)
    skill_prompt = models.TextField(blank=True, null=True, verbose_name='技能提示词')

    enable_conversation_history = models.BooleanField(default=False, verbose_name='启用对话历史')
    conversation_window_size = models.IntegerField(default=10, verbose_name='对话窗口大小')

    enable_rag = models.BooleanField(default=False, verbose_name='启用RAG')
    knowledge_base_folders = models.ManyToManyField(KnowledgeBaseFolder, blank=True, verbose_name='知识库')
    rag_top_k = models.IntegerField(default=5, verbose_name='RAG返回结果数量')
    rag_num_candidates = models.IntegerField(default=1000, verbose_name='RAG向量候选数量')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "LLM技能管理"
        verbose_name_plural = verbose_name


class EmbedModelChoices(models.TextChoices):
    FASTEMBED = 'fastembed', 'FastEmbed'
    OPENAI = 'openai', 'OpenAI'


class EmbedProvider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    embed_model = models.CharField(max_length=255, choices=EmbedModelChoices.choices, verbose_name='嵌入模型')
    embed_config = models.JSONField(verbose_name='嵌入配置', blank=True, null=True, encoder=PrettyJSONEncoder,
                                    default=dict)
    enabled = models.BooleanField(default=True, verbose_name='是否启用')

    def save(self, *args, **kwargs):
        key = base64.urlsafe_b64encode(SECRET_KEY.encode()[:32])
        cipher_suite = Fernet(key)
        if self.embed_model == EmbedModelChoices.OPENAI:
            openai_api_key = self.embed_config.get('openai_api_key')
            if openai_api_key:
                try:
                    cipher_suite.decrypt(openai_api_key.encode())
                except Exception:
                    encrypted_key = cipher_suite.encrypt(openai_api_key.encode())
                    self.embed_config['openai_api_key'] = encrypted_key.decode()
        super().save(*args, **kwargs)

    @cached_property
    def decrypted_embed_config(self):
        key = base64.urlsafe_b64encode(SECRET_KEY.encode()[:32])
        cipher_suite = Fernet(key)
        embed_config_decrypted = self.embed_config.copy()
        if self.embed_model == EmbedModelChoices.OPENAI:
            encrypted_openai_api_key = self.embed_config.get('openai_api_key')
            if encrypted_openai_api_key:
                try:
                    decrypted_key = cipher_suite.decrypt(encrypted_openai_api_key.encode())
                    embed_config_decrypted['openai_api_key'] = decrypted_key.decode()
                except Exception:
                    pass
        return embed_config_decrypted

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Embed模型"
        verbose_name_plural = verbose_name
