from django.db import models


class Rules(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='规则名称')
    description = models.TextField(null=True, blank=True, verbose_name='描述')
    rules_steps = models.TextField(null=True, blank=True, verbose_name='规则步骤')
    rules_condition = models.TextField(null=True, blank=True, verbose_name='规则条件')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "规则"
        verbose_name_plural = verbose_name
