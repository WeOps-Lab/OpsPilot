import inspect
from http.client import HTTPResponse
from typing import Text, Optional, Dict, Any, Callable, Awaitable

from loguru import logger
from rasa.core.channels import InputChannel, UserMessage
from requests import Request
from sanic import Blueprint, response

from utils.enterprise_wechat_bot_utils import EnterpriseWechatBotUtils
from utils.eventbus import EventBus


class NotificationBotChannel(InputChannel):
    def name(self) -> Text:
        return "notification_bot_channel"

    def __init__(self, enterprise_bot_url, secret_token) -> None:
        super().__init__()

        self.enterprise_bot_url = enterprise_bot_url
        self.secret_token = secret_token
        self.event_bus = EventBus()
        self.event_bus.consume('enterprise_wechat_bot_channel', self.recieve_event)
        logger.info('NotificationBotChannel init success')

    def recieve_event(self, event):
        if 'notification_content' in event:
            logger.info(f'NotificationBotChannel recieve event: {event}')
            EnterpriseWechatBotUtils.send_wechat_notification(self.enterprise_bot_url, event['notification_content'])

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get("enterprise_bot_url"),
            credentials.get("secret_token")
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
            EnterpriseWechatBotUtils.send_wechat_notification(self.enterprise_bot_url, content)
            return response.json({"status": "ok"})

        return webhook
