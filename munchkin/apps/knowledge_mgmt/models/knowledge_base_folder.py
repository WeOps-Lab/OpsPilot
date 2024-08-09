from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.utils.elasticsearch_utils import get_es_client
from django.db import models
from elasticsearch import NotFoundError
from loguru import logger

TRAIN_STATUS_CHOICES = [
    (0, "待训练"),
    (1, "处理中"),
    (2, "完成"),
    (3, "失败"),
]


class KnowledgeBaseFolder(MaintainerInfo):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    description = models.TextField(verbose_name="描述")
    embed_model = models.ForeignKey(
        "model_provider_mgmt.EmbedProvider",
        on_delete=models.CASCADE,
        verbose_name="嵌入模型",
    )

    train_status = models.IntegerField(default=0, choices=TRAIN_STATUS_CHOICES, verbose_name="状态")
    train_progress = models.FloatField(default=0, verbose_name="训练进度")

    enable_vector_search = models.BooleanField(default=True, verbose_name="向量检索")
    vector_search_weight = models.FloatField(default=0.1, verbose_name="向量检索权重")

    rag_k = models.IntegerField(default=50, verbose_name="返回结果数量")
    rag_num_candidates = models.IntegerField(default=1000, verbose_name="候选数量")

    enable_text_search = models.BooleanField(default=True, verbose_name="文本检索")
    text_search_weight = models.FloatField(default=0.9, verbose_name="文本检索权重")

    enable_rerank = models.BooleanField(default=False, verbose_name="启用Rerank")
    rerank_model = models.ForeignKey(
        "model_provider_mgmt.RerankProvider",
        on_delete=models.CASCADE,
        verbose_name="Rerank模型",
        blank=True,
        null=True,
    )
    rerank_top_k = models.IntegerField(default=10, verbose_name="Rerank返回结果数量")

    ocr_model = models.ForeignKey(
        "model_provider_mgmt.OCRProvider",
        blank=True,
        null=True,
        related_name="file_ocr_model",
        on_delete=models.CASCADE,
        verbose_name="OCR模型",
    )
    knowledge_integration = models.ManyToManyField(
        "KnowledgeIntegration",
        blank=True,
        related_name="knowledge_base_folders",
        verbose_name="知识集成",
    )

    def __str__(self):
        return self.name

    def knowledge_index_name(self):
        return f"knowledge_base_{self.id}"

    def delete(self, *args, **kwargs):
        index_name = self.knowledge_index_name()
        es_client = get_es_client()
        try:
            es_client.indices.delete(index=index_name)
            logger.info(f"Index {index_name} successfully deleted.")
        except NotFoundError:
            logger.info(f"Index {index_name} not found, skipping deletion.")

        return super().delete(*args, **kwargs)  # 调用父类的delete方法来执行实际的删除操作

    class Meta:
        verbose_name = "知识库"
        verbose_name_plural = verbose_name
