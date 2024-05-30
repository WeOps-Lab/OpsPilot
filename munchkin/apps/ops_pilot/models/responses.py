from django.db import models


class Responses(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='回复名称')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "回复"
        verbose_name_plural = verbose_name
