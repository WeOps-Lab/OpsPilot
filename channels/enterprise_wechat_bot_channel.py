import inspect
from typing import Text, Dict, Any, Optional, Callable, Awaitable

from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse

from channels.WWXRobot import WWXRobot


class EnterpriseWechatBotChannel(InputChannel):
    def name(self) -> Text:
        return "enterprise_wechat_bot"

    def __init__(self, token) -> None:
        super().__init__()
        self.token = token
        self.bot = WWXRobot(token)

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get('token'),
        )

    def blueprint(
            self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        enterprise_wechathook = Blueprint(
            "enterprise_wechat_bot_hook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @enterprise_wechathook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @enterprise_wechathook.route("/raw", methods=["POST"])
        async def msg_entry(request: Request) -> HTTPResponse:
            data = request.json
            self.bot.send_markdown(data['message'])
            return HTTPResponse()

        @enterprise_wechathook.route("/", methods=["POST"])
        async def msg_entry(request: Request) -> HTTPResponse:
            input_channel = self.name()

            data = request.json
            collector = CollectingOutputChannel()
            await on_new_message(
                UserMessage(
                    data['message'],
                    collector,
                    sender_id=data['sender_id'],
                    input_channel=input_channel,
                    metadata=None,
                )
            )
            for message in collector.messages:
                self.bot.send_markdown(message['text'])
            return HTTPResponse()

        return enterprise_wechathook
