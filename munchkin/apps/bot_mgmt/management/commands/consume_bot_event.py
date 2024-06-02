import json

import pika
from django.core.management import BaseCommand
from loguru import logger
from apps.bot_mgmt.models import Bot, BotConversationHistory
from apps.channel_mgmt.models import ChannelUser, ChannelUserGroup
from munchkin.components.conversation_mq import CONVERSATION_MQ_HOST, CONVERSATION_MQ_PORT, CONVERSATION_MQ_USER, \
    CONVERSATION_MQ_PASSWORD


class Command(BaseCommand):
    help = '获取对话历史'

    def handle(self, *args, **options):
        logger.info(f'初始化消息队列连接:[{CONVERSATION_MQ_HOST}:{CONVERSATION_MQ_PORT}]')

        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=CONVERSATION_MQ_HOST, port=CONVERSATION_MQ_PORT,
            credentials=pika.PlainCredentials(
                CONVERSATION_MQ_USER, CONVERSATION_MQ_PASSWORD
            )
        ))
        channel = connection.channel()

        bots = Bot.objects.all()
        logger.info(f'获取到{bots.count()}个机器人,开始消费消息队列......')

        for bot in bots:
            for method_frame, properties, body in channel.consume(f'bot-id-{bot.id}'):
                message = json.loads(body.decode())
                logger.debug(f'获取到消息:{message}')

                if 'text' in message:
                    sender_id = message['sender_id']
                    channel_user_exists = ChannelUser.objects.filter(user_id=sender_id).exists()
                    if channel_user_exists is False:
                        logger.info(f'用户[{sender_id}]不存在,创建用户,并加入默认用户组')
                        channel_user_group = ChannelUserGroup.objects.get(channel=bot.channels.first(),
                                                                          name='默认用户组')
                        ChannelUser.objects.create(channel_user_group=channel_user_group,
                                                   user_id=sender_id)

                    channel_user = ChannelUser.objects.get(user_id=sender_id)

                    # 创建对话历史
                    BotConversationHistory.objects.create(bot=bot, user=channel_user,
                                                          created_at=message['timestamp'],
                                                          conversation_role=message['event'],
                                                          conversation=message['text'])
                channel.basic_ack(method_frame.delivery_tag)
