from django.db import models


class ChannelUserGroup(models.Model):
    id = models.AutoField(primary_key=True)
    channel = models.ForeignKey("channel_mgmt.Channel", on_delete=models.CASCADE, verbose_name="通道")
    name = models.CharField(max_length=100, verbose_name="名称")

    class Meta:
        verbose_name = "消息通道用户组"
        verbose_name_plural = verbose_name
        unique_together = ["channel", "name"]

    def __str__(self):
        return f"{self.name}({self.channel.name})"
