from django.db import models


class SlotForm(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name='表单名称')
    slots = models.ManyToManyField('Slots', verbose_name='槽位')
    description = models.TextField(null=True, blank=True, verbose_name='描述')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "表单"
        verbose_name_plural = verbose_name
