from django.db import models

from apps.channel_mgmt.models import Channel
from apps.core.models.maintainer_info import MaintainerInfo


class Bot(MaintainerInfo):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="名称")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    channels = models.ManyToManyField(Channel, verbose_name="通道", blank=True)

    assistant_id = models.CharField(max_length=255, verbose_name="机器人ID", default="")
    rasa_model = models.ForeignKey('bot_mgmt.RasaModel', on_delete=models.CASCADE, verbose_name="模型", blank=True,
                                   null=True)

    llm_skills = models.ManyToManyField("model_provider_mgmt.LLMSkill", verbose_name="LLM技能", blank=True)
    automation_skills = models.ManyToManyField("bot_mgmt.AutomationSkill", verbose_name="自动化技能", blank=True)

    enable_bot_domain = models.BooleanField(verbose_name="启用域名", default=False)
    enable_ssl = models.BooleanField(verbose_name="启用SSL", default=False)
    bot_domain = models.CharField(max_length=255, verbose_name="域名", blank=True, null=True)

    enable_node_port = models.BooleanField(verbose_name="启用端口映射", default=False)
    node_port = models.IntegerField(verbose_name="端口映射", default=5005)

    online = models.BooleanField(verbose_name="是否上线", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "机器人"
        verbose_name_plural = verbose_name
