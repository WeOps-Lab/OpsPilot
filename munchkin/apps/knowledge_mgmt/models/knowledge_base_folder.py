from django.db import models

TRAIN_STATUS_CHOICES = [
    (0, '待训练'),
    (1, '处理中'),
    (2, '完成'),
    (3, '失败'),
]


class KnowledgeBaseFolder(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    description = models.TextField(verbose_name='描述')
    embed_model = models.ForeignKey('model_provider_mgmt.EmbedProvider', on_delete=models.CASCADE,
                                    verbose_name='嵌入模型')

    train_status = models.IntegerField(default=0, choices=TRAIN_STATUS_CHOICES, verbose_name='状态')
    train_progress = models.FloatField(default=0, verbose_name='训练进度')

    enable_general_parse = models.BooleanField(default=True, verbose_name='分块解析')
    general_parse_chunk_size = models.IntegerField(default=256, verbose_name='分块大小')
    general_parse_chunk_overlap = models.IntegerField(default=32, verbose_name='分块重叠')

    enable_vector_search = models.BooleanField(default=True, verbose_name='向量检索')
    vector_search_weight = models.FloatField(default=0.1, verbose_name='向量检索权重')

    rag_k = models.IntegerField(default=50, verbose_name='返回结果数量')
    rag_num_candidates = models.IntegerField(default=1000, verbose_name='候选数量')

    enable_text_search = models.BooleanField(default=True, verbose_name='文本检索')
    text_search_weight = models.FloatField(default=0.9, verbose_name='文本检索权重')

    enable_rerank = models.BooleanField(default=False, verbose_name='启用Rerank')
    rerank_model = models.ForeignKey('model_provider_mgmt.RerankProvider', on_delete=models.CASCADE,
                                     verbose_name='Rerank模型', blank=True,
                                     null=True)
    rerank_top_k = models.IntegerField(default=10, verbose_name='Rerank返回结果数量')

    def __str__(self):
        return self.name

    def knowledge_index_name(self):
        return f"knowledge_base_{self.id}"

    class Meta:
        verbose_name = "知识库"
        verbose_name_plural = verbose_name
