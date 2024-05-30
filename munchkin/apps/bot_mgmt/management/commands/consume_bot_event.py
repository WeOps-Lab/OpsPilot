import json

import pika
from django.core.management import BaseCommand

from apps.bot_mgmt.models import Bot, BotConversationHistory
from apps.channel_mgmt.models import ChannelUser, ChannelUserGroup


class Command(BaseCommand):
    help = '获取对话历史'

    def handle(self, *args, **options):
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost', port=5672, credentials=pika.PlainCredentials('admin', 'password')
        ))
        channel = connection.channel()
        bots = Bot.objects.all()

        for bot in bots:
            for method_frame, properties, body in channel.consume(f'bot-id-{bot.id}'):
                message = json.loads(body.decode())
                # 查询通道下的用户表有没有这个sender_id,没有则创建
                if 'text' in message:
                    channel_user_exists = ChannelUser.objects.filter(user_id=message['sender_id']).exists()
                    if channel_user_exists is False:
                        channel_user_group = ChannelUserGroup.objects.get(channel=bot.channels.first(),
                                                                          name='默认用户组')
                        ChannelUser.objects.create(channel_user_group=channel_user_group,
                                                   user_id=message['sender_id'])

                    channel_user = ChannelUser.objects.get(user_id=message['sender_id'])

                    # 创建对话历史
                    BotConversationHistory.objects.create(bot=bot, user=channel_user,
                                                          created_at=message['timestamp'],
                                                          conversation_role=message['event'],
                                                          conversation=message['text'])
                channel.basic_ack(method_frame.delivery_tag)
