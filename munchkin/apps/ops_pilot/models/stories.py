from django.db import models


class Stories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='故事名称')
    description = models.TextField(null=True, blank=True, verbose_name='描述')
    story_steps = models.TextField(null=True, blank=True, verbose_name='故事步骤')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "故事"
        verbose_name_plural = verbose_name
