from django.db import models


class WebPageKnowledge(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='标题')
    url = models.URLField(verbose_name='URL')
    knowledge_base_folder = models.ForeignKey('knowledge_mgmt.KnowledgeBaseFolder', verbose_name='知识', blank=True,
                                              null=True,
                                              on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "网页知识"
        verbose_name_plural = verbose_name
