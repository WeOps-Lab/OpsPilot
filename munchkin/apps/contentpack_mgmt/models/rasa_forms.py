from django.db import models
from django_yaml_field import YAMLField

from apps.core.models.maintainer_info import MaintainerInfo


class RasaForms(MaintainerInfo):
    id = models.AutoField(primary_key=True)
    content_pack = models.ForeignKey('contentpack_mgmt.ContentPack', on_delete=models.CASCADE, verbose_name='扩展包')
    name = models.CharField(max_length=255, verbose_name='表单名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    form = YAMLField(verbose_name='表单', default={
        "form_name": {
            "required_slots": ["slot_name"],
        }
    })

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '表单'
        verbose_name_plural = verbose_name
