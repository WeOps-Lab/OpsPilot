from django.db import models


class ManualKnowledge(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    knowledge_base_folder = models.ForeignKey('knowledge_mgmt.KnowledgeBaseFolder', verbose_name='知识', blank=True,
                                              null=True,
                                              on_delete=models.CASCADE)
    custom_metadata = models.JSONField(verbose_name='自定义元数据', blank=True, null=True, default=dict)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "手工录入"
        verbose_name_plural = verbose_name
