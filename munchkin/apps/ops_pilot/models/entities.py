from django.db import models


class Entities(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='实体名称')
    description = models.TextField(verbose_name='实体描述', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "实体"
        verbose_name_plural = verbose_name
