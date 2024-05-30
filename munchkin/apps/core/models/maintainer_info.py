from django.db import models


class MaintainerInfo(models.Model):
    """
    Add maintainer fields to another models.
    """

    class Meta:
        verbose_name = "维护者相关字段"
        abstract = True

    created_user_id = models.CharField("创建者ID", max_length=32, default="")
    updated_user_id = models.CharField("更新者ID", max_length=32, default="")
