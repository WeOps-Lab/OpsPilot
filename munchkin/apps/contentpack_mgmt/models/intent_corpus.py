from django.db import models

from apps.core.models.maintainer_info import MaintainerInfo


class IntentCorpus(MaintainerInfo):
    id = models.AutoField(primary_key=True)
    intent = models.ForeignKey('contentpack_mgmt.Intent', on_delete=models.CASCADE, verbose_name='意图')
    corpus = models.TextField(verbose_name='语料')

    def __str__(self):
        return self.corpus

    class Meta:
        verbose_name = '意图语料'
        verbose_name_plural = verbose_name
