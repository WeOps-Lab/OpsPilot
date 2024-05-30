from django.db import models

from apps.channel_mgmt.models import Channel, ChannelUserGroup, ChannelUser
from apps.contentpack_mgmt.models import RasaModel
from apps.knowledge_mgmt.models import KnowledgeBaseFolder
from apps.model_provider_mgmt.models import LLMModel
from django_yaml_field import YAMLField


class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    channels = models.ManyToManyField(Channel, verbose_name='通道', blank=True, null=True)

    assistant_id = models.CharField(max_length=255, verbose_name='机器人ID', default='')
    rasa_model = models.ForeignKey(RasaModel, on_delete=models.CASCADE, verbose_name='模型', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '机器人'
        verbose_name_plural = verbose_name


BOT_CONVERSATION_ROLE_CHOICES = [
    ('user', '用户'),
    ('bot', '机器人')
]


class BotConversationHistory(models.Model):
    id = models.AutoField(primary_key=True)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, verbose_name='机器人')
    user = models.ForeignKey(ChannelUser, on_delete=models.CASCADE, verbose_name='用户')
    conversation_role = models.CharField(max_length=255, verbose_name='对话角色',
                                         choices=BOT_CONVERSATION_ROLE_CHOICES)
    conversation = models.TextField(verbose_name='对话内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.conversation

    class Meta:
        verbose_name = '对话历史'
        verbose_name_plural = verbose_name
