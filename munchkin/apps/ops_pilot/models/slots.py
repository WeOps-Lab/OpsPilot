from django.db import models


class Slots(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='槽位名称')
    slot_type = models.CharField(max_length=255, verbose_name='槽位类型')
    influence_conversation = models.BooleanField(default=False, verbose_name='是否影响对话')
    description = models.TextField(verbose_name='槽位描述', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "槽位"
        verbose_name_plural = verbose_name
