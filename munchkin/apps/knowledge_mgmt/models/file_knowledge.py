from django.core.validators import FileExtensionValidator
from django.db import models
from django_minio_backend import MinioBackend, iso_date_prefix

KNKOWLEDGE_TYPES = ['md', 'docx', 'xlsx', 'csv', 'pptx', 'pdf', 'txt']


class FileKnowledge(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='文件名称')
    file = models.FileField(verbose_name="文件",
                            storage=MinioBackend(bucket_name='munchkin-private'),
                            upload_to=iso_date_prefix,
                            validators=[FileExtensionValidator(allowed_extensions=KNKOWLEDGE_TYPES)])
    custom_metadata = models.JSONField(verbose_name='自定义元数据', blank=True, null=True, default=dict)

    knowledge_base_folder = models.ForeignKey('knowledge_mgmt.KnowledgeBaseFolder', verbose_name='知识', blank=True,
                                              null=True,
                                              on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.title = self.file.name
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "文件知识"
        verbose_name_plural = verbose_name
