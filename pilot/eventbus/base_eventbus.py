import json
import threading

import pika
from loguru import logger
import requests
from requests.auth import HTTPBasicAuth

from core.server_settings import server_settings

CODE_REVIEW_EVENT = "code_review_event"


class BaseEventBus:
    def __init__(self):
        self.virtual_host_name = f'pilot_{server_settings.munchkin_bot_id}'
        self.create_virtual_host(self.virtual_host_name)

    def create_virtual_host(self, vhost_name):
        logger.info(f"Creating Virtual Host '{vhost_name}'...")
        url = f"http://{server_settings.rabbitmq_host}:15672/api/vhosts/{vhost_name}"
        auth = HTTPBasicAuth(server_settings.rabbitmq_username, server_settings.rabbitmq_password)
        headers = {'content-type': 'application/json'}

        response = requests.put(url, auth=auth, headers=headers)

        if response.status_code == 201:
            logger.info(f"Virtual Host '{vhost_name}' created successfully.")
        else:
            logger.info(f"Failed to create Virtual Host '{vhost_name}'. Status code: {response.status_code}")

    def prepare_eventbus(self):

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=server_settings.rabbitmq_host, port=server_settings.rabbitmq_port,
                                      virtual_host=self.virtual_host_name,
                                      credentials=pika.PlainCredentials(server_settings.rabbitmq_username,
                                                                        server_settings.rabbitmq_password)))
        channel = connection.channel()
        channel.exchange_declare(exchange='event_bus', exchange_type='fanout', durable=True)
        return connection, channel

    def publish(self, messages: str):
        """
        事件广播
        :param messages:
        :return:
        """
        connection, channel = self.prepare_eventbus()

        properties = pika.BasicProperties(delivery_mode=2, expiration=str(5 * 60 * 1000))

        channel.basic_publish(exchange='event_bus', routing_key='', body=messages,
                              properties=properties)
        connection.close()

    def consume(self, queue_name: str, callback_func):
        """
        事件消费
        :param queue_name:
        :param callback_func:
        :return:
        """
        connection, channel = self.prepare_eventbus()

        result = channel.queue_declare(queue=queue_name)
        channel.queue_bind(exchange='event_bus', queue=queue_name)

        def callback(ch, method, properties, body):
            try:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                obj = json.loads(body.decode())
                callback_func(obj)
            except Exception as e:
                logger.error(e)

        channel.basic_consume(result.method.queue, callback, False)
        consume_thread = threading.Thread(target=channel.start_consuming)
        consume_thread.start()
