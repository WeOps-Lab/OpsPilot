import asyncio
import inspect
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from typing import Dict, Optional, Text, Any, Callable, Awaitable

from rasa_sdk import logger
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)
from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from wechatpy.enterprise import WeChatClient, WeChatCrypto, parse_message


class EnterpriseWechatChannel(InputChannel):
    def name(self) -> Text:
        return "enterprise_wechat"

    def __init__(self, corp_id, secret, token, aes_key, agent_id) -> None:
        super().__init__()

        self.corp_id = corp_id
        self.secret = secret
        self.token = token
        self.aes_key = aes_key
        self.agent_id = agent_id
        self.thread_pool = ThreadPoolExecutor(max_workers=8)

        self.crypto = WeChatCrypto(token, aes_key, corp_id)

        self.wechat_client = WeChatClient(
            corp_id,
            secret,
        )

    @classmethod
    def from_credentials(cls, credentials: Optional[Dict[Text, Any]]) -> "InputChannel":
        return cls(
            credentials.get("corp_id"),
            credentials.get("secret"),
            credentials.get("token"),
            credentials.get("aes_key"),
            credentials.get("agent_id"),
        )

    async def send_message(self, request, query, reply_user_id):
        try:
            if not query:
                return

            context = dict()
            context['from_user_id'] = reply_user_id
            collector = CollectingOutputChannel()
            await request.app.ctx.agent.handle_message(
                UserMessage(
                    text=query,
                    output_channel=collector,
                    sender_id=reply_user_id,
                    input_channel=self.name(),
                    metadata=None,
                )
            )
            response_data = collector.messages
            reply_text = (
                "\n\n".join(data["text"] for data in response_data)
                .replace("bot:", "")
                .strip()
            )

            self.wechat_client.message.send_markdown(self.agent_id, reply_user_id, reply_text)
        except Exception as e:
            logger.exception(e)

    def blueprint(
            self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:
        enterprise_wechathook = Blueprint(
            "enterprise_wechat_hook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @enterprise_wechathook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            msg_signature = request.args.get('msg_signature')
            timestamp = request.args.get('timestamp')
            nonce = request.args.get('nonce')
            echostr = request.args.get('echostr')
            echo_str = self.crypto.check_signature(msg_signature, timestamp, nonce, echostr)
            return response.text(echo_str)

        @enterprise_wechathook.route("/", methods=["POST"])
        async def msg_entry(request: Request) -> HTTPResponse:
            query_params = request.args
            signature = query_params.get('msg_signature', '')
            timestamp = query_params.get('timestamp', '')
            nonce = query_params.get('nonce', '')

            if request.method == 'GET':
                echostr = query_params.get('echostr', '')
                echostr = self.crypto.check_signature(
                    signature, timestamp, nonce, echostr
                )
                return echostr
            elif request.method == 'POST':
                message = self.crypto.decrypt_message(
                    request.body,
                    signature,
                    timestamp,
                    nonce
                )
                msg = parse_message(message)
                if msg.type == "event":
                    return HTTPResponse(body="")

                thread = Thread(target=asyncio.run, args=(self.send_message(
                    request,
                    msg.content,
                    msg.source,
                ),))
                thread.start()

                return HTTPResponse(body="")

        return enterprise_wechathook
