from django.db import models


class OCRProvider(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, verbose_name="名称")
    ocr_config = models.JSONField(
        verbose_name="OCR配置",
        blank=True,
        null=True,
        default=dict,
    )
    enabled = models.BooleanField(default=True, verbose_name="是否启用")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "OCR模型"
        verbose_name_plural = verbose_name
