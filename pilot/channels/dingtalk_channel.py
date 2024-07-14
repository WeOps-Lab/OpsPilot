import asyncio
import inspect
import threading
from threading import Thread
from typing import Text, Optional, Dict, Any, Callable, Awaitable

from loguru import logger
from rasa.core.channels import InputChannel, CollectingOutputChannel, UserMessage
from sanic import Blueprint, Request, HTTPResponse, response

from libs import dingtalk_stream
from libs.dingtalk_stream import AckMessage
from eventbus.notification_eventbus import NotificationEventBus


class EventHandler(dingtalk_stream.EventHandler):
    async def process(self, event: dingtalk_stream.EventMessage):
        return AckMessage.STATUS_OK, 'OK'


class CallbackHandler(dingtalk_stream.ChatbotHandler):
    def __init__(self, on_new_message):
        super(dingtalk_stream.ChatbotHandler, self).__init__()
        self.on_new_message = on_new_message

    async def process(self, message: dingtalk_stream.CallbackMessage):
        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(message.data)
        text = incoming_message.text.content.strip()

        thread = Thread(target=asyncio.run, args=(self.send_message(
            self.on_new_message,
            text,
            incoming_message,
        ),))
        thread.start()

        return AckMessage.STATUS_OK, 'OK'

    async def send_message(self, on_new_message, query, incoming_message):
        collector = CollectingOutputChannel()
        await on_new_message(
            UserMessage(
                text=query,
                output_channel=collector,
                sender_id=incoming_message.sender_staff_id,
                input_channel='dingtalk',
                metadata=None,
            )
        )
        response_data = collector.messages
        reply_text = (
            "\n\n".join(data["text"] for data in response_data)
            .replace("bot:", "")
            .strip()
        )
        self.reply_markdown('title', reply_text, incoming_message)


class DingTalkChannel(InputChannel):
    def name(self) -> Text:
        return "dingtalk_channel"

    def recieve_event(self, event):
        if self.event_bus.is_notification_event(event):
            reply_user_id = self.event_bus.get_notification_event_sender_id(event)
            reply_text = self.event_bus.get_notification_event_content(event)
            logger.info(f"收到消息总线通知,目标用户:[{reply_user_id}],内容:[{reply_text}]")

            # 暂未实现

    def __init__(self, client_id, client_secret, enable_eventbus) -> None:
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.enable_eventbus = enable_eventbus

        if self.enable_eventbus:
            self.event_bus = NotificationEventBus()
            self.event_bus.consume('enterprise_wechat_bot_channel', self.recieve_event)

        logger.info('钉钉机器人通道已启动')

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get("client_id"),
            credentials.get("client_secret"),
            credentials.get("enable_eventbus")
        )

    def blueprint(
            self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        dingtalk_hook = Blueprint(
            "dingtalk_channel{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        credential = dingtalk_stream.Credential(self.client_id, self.client_secret)
        client = dingtalk_stream.DingTalkStreamClient(credential)

        client.register_all_event_handler(EventHandler())
        client.register_callback_handler(dingtalk_stream.ChatbotMessage.TOPIC, CallbackHandler(on_new_message))

        thread = threading.Thread(target=client.start_forever)
        thread.start()

        @dingtalk_hook.route("/", methods=["GET"])
        async def index(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        return dingtalk_hook
