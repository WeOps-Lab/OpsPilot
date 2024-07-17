import inspect
from http.client import HTTPResponse
from typing import Text, Optional, Dict, Any, Callable, Awaitable

import requests
from rasa.core.channels import InputChannel, UserMessage
from requests import Request
from sanic import Blueprint, response

import os

from loguru import logger

from eventbus.notification_eventbus import NotificationEventBus


class EnterpriseWechatBotChannel(InputChannel):
    def name(self) -> Text:
        return "enterprise_wechat_bot_channel"

    def __init__(self, enterprise_bot_url, secret_token, enable_eventbus) -> None:
        super().__init__()

        self.enterprise_bot_url = enterprise_bot_url
        self.secret_token = secret_token
        self.bot_id = os.getenv('MUNCHKIN_BOT_ID', "")

        if enable_eventbus:
            queue_name = f"enterprise_wechat_bot_channel_{self.bot_id}"
            logger.info(f"启动Pilot消息总线:[{queue_name}]")
            self.event_bus = NotificationEventBus()
            self.event_bus.consume(queue_name, self.process_event)

    def send_enterprise_wechat_bot_message(self, url: str, content: str):
        """
        发送企业微信机器人文本消息
        :param url:
        :param content:
        :return:
        """
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        response = requests.post(url, headers={
            'Content-Type': 'application/json'
        }, json=data, verify=False)

        return response.json()

    def process_event(self, event):
        # 接收到不属于通知类型的消息
        if self.event_bus.is_notification_event(event) is False:
            return

        # 接受到不属于本通道的消息
        if event['integration'] != "" and event['integration'] != "enterprise_wechat_bot_channel":
            return

        self.send_enterprise_wechat_bot_message(self.enterprise_bot_url,
                                                self.event_bus.get_notification_event_content(event))

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get("enterprise_bot_url"),
            credentials.get("secret_token"),
            credentials.get("enable_eventbus", False)
        )

    def blueprint(
            self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        webhook = Blueprint(
            "notification_bot_channel{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @webhook.route("/", methods=["GET"])
        async def index(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @webhook.route("/", methods=["POST"])
        async def notify(request: Request) -> HTTPResponse:
            if request.args.get('secret_token') != self.secret_token:
                return response.json({"status": "error"}, status=401)

            body = request.json
            content = body.get("content")
            self.send_enterprise_wechat_bot_message(self.enterprise_bot_url, content)
            return response.json({"status": "ok"})

        return webhook
