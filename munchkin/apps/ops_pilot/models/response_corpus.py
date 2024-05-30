from django.db import models


class ResponseCorpus(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField(verbose_name='回复')
    channel = models.CharField(max_length=255, verbose_name='渠道', null=True, blank=True)
    buttons = models.TextField(null=True, blank=True, verbose_name='按钮')
    response = models.ForeignKey('Responses', on_delete=models.CASCADE, verbose_name='回复', null=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "回复语料"
        verbose_name_plural = verbose_name
