from apps.core.models.maintainer_info import MaintainerInfo
from django.db import models


class ContentPack(MaintainerInfo):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="扩展包名称")
    description = models.TextField(verbose_name="描述", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "扩展包"
        verbose_name_plural = verbose_name
