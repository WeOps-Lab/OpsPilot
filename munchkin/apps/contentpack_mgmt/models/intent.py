from django.db import models


class Intent(models.Model):
    id = models.AutoField(primary_key=True)
    content_pack = models.ForeignKey("contentpack_mgmt.ContentPack", on_delete=models.CASCADE, verbose_name="扩展包")
    name = models.CharField(max_length=255, verbose_name="意图名称")
    description = models.TextField(blank=True, null=True, verbose_name="描述")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "意图"
        verbose_name_plural = verbose_name
