from django.db import models


class Actions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='动作名称')
    action_func = models.CharField(max_length=255, verbose_name='动作函数')
    description = models.TextField(verbose_name='动作描述', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "动作"
        verbose_name_plural = verbose_name
