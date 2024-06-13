from django.db import models
from django.contrib.auth.models import User


class MaintainerInfo(models.Model):
    """
    Add maintainer fields to another models.
    """

    created_by = models.ForeignKey(User, related_name='%(class)s_created', on_delete=models.CASCADE, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "维护者相关字段"
        abstract = True

