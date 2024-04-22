import inspect
from typing import Dict, Optional, Text, Any, Callable, Awaitable

from loguru import logger
from rasa.core.channels.channel import (
    InputChannel,
    UserMessage,
)
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse

from actions.services.chat_service import ChatService
from utils.enterprise_wechat_bot_utils import EnterpriseWechatBotUtils


class EnterpriseWeChatJenkinsNotification(InputChannel):
    def name(self) -> Text:
        return "enterprise_wechat_jenkins_notification"

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get("fastgpt_url"),
            credentials.get("fastgpt_token"),
            credentials.get("enterprise_bot_url"),
            credentials.get("secret_token")
        )

    def __init__(self, fastgpt_url, fastgpt_token, enterprise_bot_url, secret_token) -> None:
        super().__init__()

        self.fastgpt_url = fastgpt_url
        self.fastgpt_token = fastgpt_token
        self.enterprise_bot_url = enterprise_bot_url
        self.secret_token = secret_token
        self.chat_service = ChatService(self.fastgpt_url, self.fastgpt_token)

    def blueprint(
            self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        webhook = Blueprint(
            "enterprise_wechat_jenkins_notification{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @webhook.route("/", methods=["GET"])
        async def index(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @webhook.route("/", methods=["POST"])
        async def notify(request: Request) -> HTTPResponse:
            if request.args.get('secret_token') != self.secret_token:
                return response.json({"status": "error"}, status=401)

            body = request.load_json()
            status = body.get("status")
            title = body.get("title")
            content = body.get("content")
            logger.info(f"EnterpriseWeChatJenkinsNotification: {content}")

            if status != "success":
                content = self.chat_service.chat('jenkins_notifycation_bot', content)

            EnterpriseWechatBotUtils.send_wechat_notification(self.enterprise_bot_url, title + '\n' + content)

            return response.json({"status": "ok"})

        return webhook
