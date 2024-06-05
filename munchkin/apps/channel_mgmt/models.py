from django.db import models
from django.utils.functional import cached_property
from django_yaml_field import YAMLField

from apps.core.mixinx import EncryptableMixin


class CHANNEL_CHOICES(models.TextChoices):
    ENTERPRISE_WECHAT = ('enterprise_wechat', '企业微信')
    ENTERPRISE_WECHAT_BOT = ('enterprise_wechat_bot', '企业微信机器人')
    DING_TALK = ('ding_talk', '钉钉')
    WEB = ('web', 'Web')
    GITLAB = ('gitlab', 'GitLab')


class Channel(models.Model, EncryptableMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='名称')
    channel_type = models.CharField(max_length=100, choices=CHANNEL_CHOICES.choices, verbose_name='类型')
    channel_config = YAMLField(verbose_name='通道配置', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.channel_type == CHANNEL_CHOICES.GITLAB:
            self.encrypt_field('secret_token',
                               self.channel_config['channels.gitlab_review_channel.GitlabReviewChannel'])

        if self.channel_type == CHANNEL_CHOICES.DING_TALK:
            self.encrypt_field('client_id', self.channel_config['channels.dingtalk_channel.DingTalkChannel'])
            self.encrypt_field('client_secret', self.channel_config['channels.dingtalk_channel.DingTalkChannel'])

        if self.channel_type == CHANNEL_CHOICES.ENTERPRISE_WECHAT:
            self.encrypt_field('secret_token',
                               self.channel_config['channels.enterprise_wechat_channel.EnterpriseWechatChannel'])
            self.encrypt_field('aes_key',
                               self.channel_config['channels.enterprise_wechat_channel.EnterpriseWechatChannel'])
            self.encrypt_field('secret',
                               self.channel_config['channels.enterprise_wechat_channel.EnterpriseWechatChannel'])
            self.encrypt_field('token',
                               self.channel_config['channels.enterprise_wechat_channel.EnterpriseWechatChannel'])

        if self.channel_type == CHANNEL_CHOICES.ENTERPRISE_WECHAT_BOT:
            self.encrypt_field('secret_token',
                               self.channel_config['channels.enterprise_wechat_bot_channel.EnterpriseWechatBotChannel'])

        super().save(*args, **kwargs)

    @cached_property
    def decrypted_channel_config(self):
        decrypted_config = self.channel_config.copy()
        if self.channel_type == CHANNEL_CHOICES.GITLAB:
            self.decrypt_field('secret_token', decrypted_config['channels.gitlab_review_channel.GitlabReviewChannel'])

        if self.channel_type == CHANNEL_CHOICES.DING_TALK:
            self.decrypt_field('client_id', decrypted_config['channels.dingtalk_channel.DingTalkChannel'])
            self.decrypt_field('client_secret', decrypted_config['channels.dingtalk_channel.DingTalkChannel'])

        if self.channel_type == CHANNEL_CHOICES.ENTERPRISE_WECHAT:
            self.decrypt_field('secret_token',
                               decrypted_config['channels.enterprise_wechat_channel.EnterpriseWechatChannel'])
            self.decrypt_field('aes_key',
                               decrypted_config['channels.enterprise_wechat_channel.EnterpriseWechatChannel'])
            self.decrypt_field('secret', decrypted_config['channels.enterprise_wechat_channel.EnterpriseWechatChannel'])
            self.decrypt_field('token', decrypted_config['channels.enterprise_wechat_channel.EnterpriseWechatChannel'])

        if self.channel_type == CHANNEL_CHOICES.ENTERPRISE_WECHAT_BOT:
            self.decrypt_field('secret_token',
                               decrypted_config['channels.enterprise_wechat_bot_channel.EnterpriseWechatBotChannel'])

        return decrypted_config

    class Meta:
        verbose_name = '消息通道'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ChannelUserGroup(models.Model):
    id = models.AutoField(primary_key=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name='通道')
    name = models.CharField(max_length=100, verbose_name='名称')

    class Meta:
        verbose_name = '消息通道用户组'
        verbose_name_plural = verbose_name
        unique_together = ['channel', 'name']

    def __str__(self):
        return f'{self.name}({self.channel.name})'


class ChannelUser(models.Model):
    id = models.AutoField(primary_key=True)
    channel_user_group = models.ForeignKey(ChannelUserGroup, on_delete=models.CASCADE, verbose_name='通道用户组')
    user_id = models.CharField(max_length=100, verbose_name='用户ID')
    name = models.CharField(max_length=100, verbose_name='名称', blank=True, null=True)

    class Meta:
        verbose_name = '消息通道用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user_id}({self.channel_user_group.name})'
