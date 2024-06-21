from apps.channel_mgmt.models import ChannelUser
from apps.core.models.maintainer_info import MaintainerInfo
from django.db import models


class BotSkillRule(MaintainerInfo):
    id = models.AutoField(primary_key=True)
    bot_id = models.ForeignKey("bot_mgmt.Bot", on_delete=models.CASCADE, verbose_name="机器人", blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name="规则名称")
    channel = models.ForeignKey("channel_mgmt.Channel", on_delete=models.CASCADE, verbose_name="生效通道", blank=True)
    rule_user_groups = models.ManyToManyField("channel_mgmt.ChannelUserGroup", verbose_name="生效用户组", blank=True)
    rule_user = models.ManyToManyField(ChannelUser, verbose_name="生效用户", blank=True)
    description = models.TextField(blank=True, null=True, verbose_name="描述")

    overwrite_skill_id = models.CharField(max_length=255, verbose_name="覆盖技能ID", blank=True, null=True)
    llm_skill = models.ForeignKey("model_provider_mgmt.LLMSkill", on_delete=models.CASCADE, verbose_name="LLM技能",
                                  blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "动作规则"
        verbose_name_plural = verbose_name
