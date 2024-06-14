from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from django.db import models


class WebPageKnowledge(TimeInfo, MaintainerInfo):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="标题")
    url = models.URLField(verbose_name="URL")
    knowledge_base_folder = models.ForeignKey(
        "knowledge_mgmt.KnowledgeBaseFolder",
        verbose_name="知识",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    custom_metadata = models.JSONField(verbose_name="自定义元数据", blank=True, null=True, default=dict)
    max_depth = models.IntegerField(verbose_name="最大深度", default=1)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "网页知识"
        verbose_name_plural = verbose_name
