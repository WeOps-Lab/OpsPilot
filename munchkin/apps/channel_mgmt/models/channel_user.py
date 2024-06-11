from django.db import models


class ChannelUser(models.Model):
    id = models.AutoField(primary_key=True)
    channel_user_group = models.ForeignKey('channel_mgmt.ChannelUserGroup', on_delete=models.CASCADE,
                                           verbose_name='通道用户组')
    user_id = models.CharField(max_length=100, verbose_name='用户ID')
    name = models.CharField(max_length=100, verbose_name='名称', blank=True, null=True)

    class Meta:
        verbose_name = '消息通道用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user_id}({self.channel_user_group.name})'
