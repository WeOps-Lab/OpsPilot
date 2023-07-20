import inspect
import os
from typing import Text, Dict, Any, Optional, Callable, Awaitable
from loguru import logger
import openai
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from actions.utils.langchain_utils import query_chatgpt


from channels.enterprise_wechat_app import QYWXApp

openai.api_key = os.getenv("OPENAI_API_KEY")


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
            qywx_app = QYWXApp(
                token=self.token,
                encoding_aes_key=self.encoding_aes_key,
                corp_id=self.corp_id,
                secret=self.secret,
                agent_id=self.agent_id,
            )

            user_id, msg_type, msg_content = qywx_app.request_decrypt(request)
            if msg_type == "event":
                # TODO:考虑在用户每天第一次进入企微应用时随机发一句话（运维知识，开发知识，时间管理知识，office操作技巧，各种冷知识等等），提升趣味性
                return HTTPResponse()

            # 直接走openai接口
            msg_content = msg_content.strip().lower()
            if "gpt" in msg_content:
                system_prompt = "You are ChatGPT, a large language model trained by OpenAI. Answer as detailed as possible."
                # 直接走chatGPT接口
                res = query_chatgpt(system_prompt, msg_content.strip("gpt"))
                qywx_app.post_msg(user_id=user_id, content=res)
                return HTTPResponse()
            if "dall" in msg_content:
                # 直接走DALL-E接口
                qywx_app.post_dall_e_img(user_id, msg_content)
                return HTTPResponse()
            
            # 走rasa处理
            sender_id = user_id
            message = msg_content
            input_channel = self.name()
            metadata = None

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

            response_data = collector.messages
            for data in response_data:
                qywx_app.post_msg(user_id=user_id, msgtype="text", content=data['text'])
            return HTTPResponse()

        return enterprise_wechathook
