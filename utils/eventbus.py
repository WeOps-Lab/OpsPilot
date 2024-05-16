import json
import threading

import pika
from loguru import logger

from actions.constants.server_settings import server_settings


class EventBus:
    def publish(self, messages):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=server_settings.rabbitmq_host, port=server_settings.rabbitmq_port,

                                      credentials=pika.PlainCredentials(server_settings.rabbitmq_username,
                                                                        server_settings.rabbitmq_password)))
        channel = connection.channel()
        channel.exchange_declare(exchange='event_bus', exchange_type='fanout', durable=True)

        channel.basic_publish(exchange='event_bus', routing_key='', body=messages,
                              properties=pika.BasicProperties(delivery_mode=2))
        connection.close()

    def consume(self, queue_name, func):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=server_settings.rabbitmq_host, port=server_settings.rabbitmq_port,

                                      credentials=pika.PlainCredentials(server_settings.rabbitmq_username,
                                                                        server_settings.rabbitmq_password)))
        channel = connection.channel()
        channel.exchange_declare(exchange='event_bus', exchange_type='fanout', durable=True)

        result = channel.queue_declare(queue=queue_name)
        channel.queue_bind(exchange='event_bus', queue=queue_name)

        def callback(ch, method, properties, body):
            try:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                obj = json.loads(body.decode())
                func(obj)
            except Exception as e:
                logger.error(e)

        channel.basic_consume(result.method.queue, callback, False)
        consume_thread = threading.Thread(target=channel.start_consuming)
        consume_thread.start()
