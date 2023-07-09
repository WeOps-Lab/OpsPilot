import inspect
import json
from typing import Text, Dict, Any, Optional, Callable, Awaitable

from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse


class EnterpriseWechatChannel(InputChannel):
    def name(self) -> Text:
        return "enterprise_wechat"

    def __init__(self, url) -> None:
        super().__init__()
        self.url = url

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get('url')
        )

    def blueprint(
            self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        enterprise_wechathook = Blueprint(
            "enterprise_wechat_hook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @enterprise_wechathook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "ok"})

        @enterprise_wechathook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            sender_id = request.json.get("sender")
            message = request.json.get("message")
            input_channel = self.name()
            metadata = self.get_metadata(request)

            collector = CollectingOutputChannel()

            await on_new_message(
                UserMessage(
                    message,
                    collector,
                    sender_id=sender_id,
                    input_channel=input_channel,
                    metadata=metadata,
                )
            )

            response_data = json.dumps(collector.messages, ensure_ascii=False)
            return response.text(response_data, content_type='application/json; charset=utf-8')

        return enterprise_wechathook
