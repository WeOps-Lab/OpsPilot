from apps.core.models.maintainer_info import MaintainerInfo
from django.db import models
from django_yaml_field import YAMLField


class RasaSlots(MaintainerInfo):
    id = models.AutoField(primary_key=True)
    content_pack = models.ForeignKey("contentpack_mgmt.ContentPack", on_delete=models.CASCADE, verbose_name="扩展包")
    name = models.CharField(max_length=255, verbose_name="槽位名称")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    slot = YAMLField(
        verbose_name="槽位",
        default={
            "slot_name": {
                "type": "text",
                "influence_conversation": True,
                "mappings": [{"type": "custom"}],
            }
        },
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "槽位"
        verbose_name_plural = verbose_name
