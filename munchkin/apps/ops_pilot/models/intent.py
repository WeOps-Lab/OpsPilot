from django.db import models


class Intent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='意图名称')
    description = models.TextField(verbose_name='意图描述', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "意图"
        verbose_name_plural = verbose_name
