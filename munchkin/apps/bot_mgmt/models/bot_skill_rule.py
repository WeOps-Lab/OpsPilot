from apps.channel_mgmt.models import ChannelUser
from django.db import models


class BotSkillRule(models.Model):
    id = models.AutoField(primary_key=True)
    bot_id = models.ForeignKey(
        "bot_mgmt.Bot",
        on_delete=models.CASCADE,
        verbose_name="机器人",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255, verbose_name="规则名称")
    skill = models.ForeignKey("model_provider_mgmt.LLMSkill", on_delete=models.CASCADE, verbose_name="LLM技能")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    prompt = models.TextField(blank=True, null=True, verbose_name="提示词")
    channel = models.ForeignKey(
        "channel_mgmt.Channel",
        on_delete=models.CASCADE,
        verbose_name="生效通道",
        blank=True,
    )
    rule_user_groups = models.ManyToManyField("channel_mgmt.ChannelUserGroup", verbose_name="生效用户组", blank=True)
    rule_user = models.ManyToManyField(ChannelUser, verbose_name="生效用户", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "动作规则"
        verbose_name_plural = verbose_name
