from django.core.validators import FileExtensionValidator
from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix

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

    class Meta:
        verbose_name = "知识库"
        verbose_name_plural = verbose_name


class ManualKnowledge(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    knowledge_base_folder = models.ForeignKey(KnowledgeBaseFolder, verbose_name='知识', blank=True, null=True,
                                              on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "手工录入"
        verbose_name_plural = verbose_name


class WebPageKnowledge(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='标题')
    url = models.URLField(verbose_name='URL')
    knowledge_base_folder = models.ForeignKey(KnowledgeBaseFolder, verbose_name='知识', blank=True, null=True,
                                              on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "网页知识"
        verbose_name_plural = verbose_name


KNKOWLEDGE_TYPES = ['md', 'docx', 'xlsx', 'csv', 'pptx', 'pdf', 'txt']


class FileKnowledge(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='文件名称')
    file = models.FileField(verbose_name="文件",
                            storage=MinioBackend(bucket_name='munchkin-private'),
                            upload_to=iso_date_prefix,
                            validators=[FileExtensionValidator(allowed_extensions=KNKOWLEDGE_TYPES)])

    knowledge_base_folder = models.ForeignKey(KnowledgeBaseFolder, verbose_name='知识', blank=True, null=True,
                                              on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.title = self.file.name
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "文件知识"
        verbose_name_plural = verbose_name
