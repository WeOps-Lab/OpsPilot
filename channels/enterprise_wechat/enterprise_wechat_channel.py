import asyncio
import inspect
import json
from threading import Thread
from typing import Dict, Optional, Text, Any, Callable, Awaitable
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse

from channels.enterprise_wechat.enterprise_wechat_app import EnterpriseWechatApp


class EnterpriseWechatChannel(InputChannel):

    def name(self) -> Text:
        return "enterprise_wechat"

    def __init__(self, token, encoding_aes_key, corp_id, secret, agent_id) -> None:
        super().__init__()
        self.token = token
        self.encoding_aes_key = encoding_aes_key
        self.corp_id = corp_id
        self.secret = secret
        self.agent_id = agent_id
        self.app = EnterpriseWechatApp(token, encoding_aes_key, corp_id, secret, agent_id)

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get("token"),
            credentials.get("encoding_aes_key"),
            credentials.get("corp_id"),
            credentials.get("secret"),
            credentials.get("agent_id"),
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

        @enterprise_wechathook.route("/", methods=["POST"])
        async def msg_entry(request: Request) -> HTTPResponse:
            user_id, msg_type, msg_content = self.app.request_decrypt(request)

            if msg_type == "event":
                # 这里返回的不是''，企微就会认为消息没有送达，会重复发送请求
                return HTTPResponse(body="")

            msg_content = msg_content.strip().lower()

            # if "km" in msg_content:
            #     self.app.post_msg(user_id=user_id, content="OpsPilot正在思考中，请稍等...")
            #
            #     qywx_app.qywx_km_qa(
            #         user_id=user_id, query=msg_content.strip("km").strip()
            #     )
            #     return HTTPResponse(body="")

            # 走rasa处理
            collector = CollectingOutputChannel()
            thread = Thread(target=asyncio.run, args=(self.app.qywx_rasa_qa(
                request,
                user_id=user_id,
                msg_content=msg_content,
                collector=collector,
                input_channel=self.name()
            ),))
            thread.start()

            return HTTPResponse(body="")

        return enterprise_wechathook
