import inspect
import json
from typing import Text, Dict, Any, Optional, Callable, Awaitable
from loguru import logger
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse

from channels.WXBizMsgCrypt3 import WXBizMsgCrypt
import xml.etree.cElementTree as ET

from channels.enterprise_wechat_utils import post_message
from actions.constant.server_settings import server_settings


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

        @enterprise_wechathook.route("/", methods=["POST"])
        async def msg_entry(request: Request) -> HTTPResponse:
            # 企微消息解析
            msg_signature = request.args["msg_signature"]
            timestamp = request.args["timestamp"]
            nonce = request.args["nonce"]
            data = request.data
            wxcpt = WXBizMsgCrypt(
                server_settings.qywx_access_token,
                server_settings.qywx_encoding_aes_key,
                server_settings.qywx_corp_id,
            )
            _, msg = wxcpt.DecryptMsg(data, msg_signature, timestamp, nonce)
            xml_tree = ET.fromstring(msg)

            # 消息类型，event表示用户进入应用，text表示用户发送消息
            msg_type = xml_tree.find("MsgType").text
            if msg_type == "event":
                return None
            if msg_type == "text":
                msg_content = xml_tree.find("Content").text
                logger.info(msg_content)
            # 企微用户id
            user_id = xml_tree.find("FromUserName").text

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
            response_data = json.dumps(collector.messages, ensure_ascii=False)
            post_message(user_id, response_data)
            return None
