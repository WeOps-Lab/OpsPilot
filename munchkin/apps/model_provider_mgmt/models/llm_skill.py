from apps.core.models.maintainer_info import MaintainerInfo
from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from django.db import models


class LLMSkillTypeChoices(models.TextChoices):
    OPEN_DOMAIN_QA = 'action_llm_fallback', '开放领域问答'


class LLMSkill(MaintainerInfo):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    llm_model = models.ForeignKey(
        "model_provider_mgmt.LLMModel", on_delete=models.CASCADE, verbose_name="LLM模型", blank=True, null=True
    )
    skill_id = models.CharField(max_length=255, verbose_name="技能ID", blank=True, null=True)
    skill_prompt = models.TextField(blank=True, null=True, verbose_name="技能提示词")

    enable_conversation_history = models.BooleanField(default=False, verbose_name="启用对话历史")
    conversation_window_size = models.IntegerField(default=10, verbose_name="对话窗口大小")

    enable_rag = models.BooleanField(default=False, verbose_name="启用RAG")
    knowledge_base_folders = models.ManyToManyField(KnowledgeBaseFolder, blank=True, verbose_name="知识库")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "LLM技能管理"
        verbose_name_plural = verbose_name
