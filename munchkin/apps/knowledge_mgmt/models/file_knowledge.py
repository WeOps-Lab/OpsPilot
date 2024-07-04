import base64

from apps.core.models.maintainer_info import MaintainerInfo
from apps.core.models.time_info import TimeInfo
from django.core.validators import FileExtensionValidator
from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix

KNKOWLEDGE_TYPES = ["md", "docx", "xlsx", "csv", "pptx", "pdf", "txt"]


class FileKnowledge(TimeInfo, MaintainerInfo):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="文件名称")
    file = models.FileField(
        verbose_name="文件",
        storage=MinioBackend(bucket_name="munchkin-private"),
        upload_to=iso_date_prefix,
        validators=[FileExtensionValidator(allowed_extensions=KNKOWLEDGE_TYPES)],
    )
    custom_metadata = models.JSONField(verbose_name="自定义元数据", blank=True, null=True, default=dict)

    knowledge_base_folder = models.ForeignKey(
        "knowledge_mgmt.KnowledgeBaseFolder",
        verbose_name="知识",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    enable_general_parse = models.BooleanField(default=True, verbose_name="分块解析")
    general_parse_chunk_size = models.IntegerField(default=256, verbose_name="分块大小")
    general_parse_chunk_overlap = models.IntegerField(default=32, verbose_name="分块重叠")

    enable_semantic_chunck_parse = models.BooleanField(default=False, verbose_name="语义分块解析")
    semantic_chunk_parse_embedding_model = models.ForeignKey('model_provider_mgmt.EmbedProvider',
                                                             blank=True, null=True,
                                                             related_name='file_semantic_chunk_parse_embedding_model',
                                                             on_delete=models.CASCADE, verbose_name='嵌入模型')

    excel_header_row_parse = models.BooleanField(default=False, verbose_name="Excel表头+行组合解析")
    excel_full_content_parse = models.BooleanField(default=True, verbose_name="Excel全内容解析")


    def __str__(self):
        return self.title

    def get_file_base64(self):
        return base64.b64encode(self.file.read()).decode('utf-8')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.title = self.file.name
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "文件知识"
        verbose_name_plural = verbose_name
