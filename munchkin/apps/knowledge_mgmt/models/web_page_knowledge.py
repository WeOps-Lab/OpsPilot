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

    enable_general_parse = models.BooleanField(default=True, verbose_name="分块解析")
    general_parse_chunk_size = models.IntegerField(default=256, verbose_name="分块大小")
    general_parse_chunk_overlap = models.IntegerField(default=32, verbose_name="分块重叠")

    enable_semantic_chunck_parse = models.BooleanField(default=False, verbose_name="语义分块解析")
    semantic_chunk_parse_embedding_model = models.ForeignKey('model_provider_mgmt.EmbedProvider',
                                                             blank=True, null=True,
                                                             related_name='semantic_chunk_parse_embedding_model',
                                                             on_delete=models.CASCADE, verbose_name='嵌入模型')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "网页知识"
        verbose_name_plural = verbose_name
