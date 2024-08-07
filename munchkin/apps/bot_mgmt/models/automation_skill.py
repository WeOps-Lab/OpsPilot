from apps.core.mixinx import EncryptableMixin
from apps.core.models.maintainer_info import MaintainerInfo
from django.db import models
from django.utils.functional import cached_property
from django_yaml_field import YAMLField


class AUTOMATION_SKILL_CHOICES(models.TextChoices):
    SALT_STACK = ("salt_stack", "SaltStack")


class AutomationSkill(MaintainerInfo, EncryptableMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="名称")
    skill_id = models.CharField(max_length=100, verbose_name="技能ID", unique=True)
    skill_type = models.CharField(max_length=100, choices=AUTOMATION_SKILL_CHOICES.choices, verbose_name="类型")
    integration = models.ForeignKey("Integration", on_delete=models.CASCADE, verbose_name="集成", blank=True, null=True)

    """
    SaltStack参数示例:
        --- yaml
            client: "local"
            tgt: "*"
            func: "cmd.run"
            args: "ls -l"
    """
    skill_config = YAMLField(verbose_name="技能配置", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "自动化技能"
        verbose_name_plural = verbose_name
