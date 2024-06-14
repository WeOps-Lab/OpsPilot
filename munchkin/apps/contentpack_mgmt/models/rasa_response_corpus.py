from django.db import models


class RasaResponseCorpus(models.Model):
    id = models.AutoField(primary_key=True)
    response = models.ForeignKey("contentpack_mgmt.RasaResponse", on_delete=models.CASCADE, verbose_name="回复")
    corpus = models.TextField(verbose_name="语料")

    def __str__(self):
        return self.corpus

    class Meta:
        verbose_name = "回复语料"
        verbose_name_plural = verbose_name
