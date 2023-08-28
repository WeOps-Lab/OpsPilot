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

from channels.enterprise_wechat_app import qywx_app


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

        @enterprise_wechathook.route("/km_search", methods=["POST"])
        async def km_search(request: Request) -> HTTPResponse:
            km_query = request.json.get("km_query")
            top_n = request.json.get("top_n")
            # 内部km标题搜索
            sim_query, link = qywx_app.km_qa(query=km_query, top_n=top_n)
            res = dict(zip(sim_query, link))
            return HTTPResponse(json.dumps(res), content_type="application/json")

        @enterprise_wechathook.route("/", methods=["POST"])
        async def msg_entry(request: Request) -> HTTPResponse:
            user_id, msg_type, msg_content = qywx_app.request_decrypt(request)

            if msg_type == "event":
                # 这里返回的不是''，企微就会认为消息没有送达，会重复发送请求
                qywx_app.post_funny_msg(user_id)
                return HTTPResponse(body="")

            # 直接走openai接口
            msg_content = msg_content.strip().lower()
            if "gpt" in msg_content:
                qywx_app.post_msg(user_id=user_id, content="AIOps智慧狗正在思考中，请稍等...")
                qywx_app.post_chatgpt_answer(user_id, msg_content)
                return HTTPResponse(body="")
            if "dall" in msg_content:
                # 直接走DALL-E接口
                qywx_app.post_msg(user_id=user_id, content="dall-e暂停支持")
                return HTTPResponse(body="")
            if "km" in msg_content:
                qywx_app.post_msg(user_id=user_id, content="AIOps智慧狗正在思考中，请稍等...")
                # 内部km搜索
                qywx_app.qywx_km_qa(
                    user_id=user_id, query=msg_content.strip("km").strip()
                )
                return HTTPResponse(body="")

            # 拉群判断
            if msg_content in [str(i) for i in range(1, 15)]:
                qywx_app.judge_create_helper_group(user_id=user_id, msg_content=msg_content)
                return HTTPResponse(body="")

            # 走rasa处理
            collector = CollectingOutputChannel()
            thread = Thread(target=asyncio.run, args=(qywx_app.qywx_rasa_qa(
                request,
                user_id=user_id,
                msg_content=msg_content,
                collector=collector,
                input_channel=self.name()
            ),))
            thread.start()

            return HTTPResponse(body="")

        return enterprise_wechathook
