from django.db import models


class IntentCorpus(models.Model):
    id = models.AutoField(primary_key=True)
    intent = models.ForeignKey('Intent', on_delete=models.CASCADE, verbose_name='意图')
    corpus = models.TextField(verbose_name='语料')

    def __str__(self):
        return self.corpus

    class Meta:
        verbose_name = "语料"
        verbose_name_plural = verbose_name
