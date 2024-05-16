import json
import threading

import pika

from actions.constants.server_settings import server_settings


class EventBus:
    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=server_settings.rabbitmq_host, port=server_settings.rabbitmq_port,
                                      credentials=pika.PlainCredentials(server_settings.rabbitmq_username,
                                                                        server_settings.rabbitmq_password)))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange='event_bus', exchange_type='fanout', durable=True)

    def publish(self, messages):
        self.channel.basic_publish(exchange='event_bus', routing_key='', body=messages,
                                   properties=pika.BasicProperties(delivery_mode=2))

    def consume(self, queue_name, func):
        result = self.channel.queue_declare(queue=queue_name)
        self.channel.queue_bind(exchange='event_bus', queue=queue_name)

        def callback(ch, method, properties, body):
            ch.basic_ack(delivery_tag=method.delivery_tag)
            obj = json.loads(body.decode())
            func(obj)

        self.channel.basic_consume(result.method.queue, callback, False)
        consume_thread = threading.Thread(target=self.channel.start_consuming)
        consume_thread.start()
