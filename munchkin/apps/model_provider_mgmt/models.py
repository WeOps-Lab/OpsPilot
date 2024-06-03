from django.db import models

from apps.core.encoders import PrettyJSONEncoder
from apps.knowledge_mgmt.models import KnowledgeBaseFolder


class LLMModelChoices(models.TextChoices):
    GPT35_16K = 'gpt-3.5-turbo-16k', 'GPT-3.5 Turbo 16K'


class LLMModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    llm_model = models.CharField(max_length=255, choices=LLMModelChoices.choices, verbose_name='LLM模型')
    llm_config = models.JSONField(verbose_name='LLM配置', blank=True, null=True, encoder=PrettyJSONEncoder,
                                  default=dict)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Embed模型"
        verbose_name_plural = verbose_name
