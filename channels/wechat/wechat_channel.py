import inspect
import io
from concurrent.futures import ThreadPoolExecutor
from typing import Text, Callable, Awaitable

import itchat
import requests
from rasa.core.channels import InputChannel, UserMessage
from rasa_sdk import logger
from sanic import Blueprint, Request, HTTPResponse, response


class WechatChannel(InputChannel):
    def name(self) -> Text:
        return "wechat"

    def __init__(self) -> None:
        super().__init__()
        self.thread_pool = ThreadPoolExecutor(max_workers=8)
        self.single_chat_prefix = ''
        self.image_create_prefix = ''
        self.group_chat_prefix = ''
        self.group_at_off = False
        self.group_chat_keyword = ''
        self.group_name_white_list = []
        self.group_name_keyword_white_list = []
        self.single_chat_reply_prefix = ''
        itchat.auto_login(enableCmdQR=2)
        itchat.run()


def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
) -> Blueprint:
    wechathook = Blueprint(
        "wechat_hook_{}".format(type(self).__name__),
        inspect.getmodule(self).__name__,
    )

    @wechathook.route("/", methods=["GET"])
    async def health(request: Request) -> HTTPResponse:
        return response.json({"status": "ok"})

    @wechathook.route("/", methods=["POST"])
    async def msg_entry(request: Request) -> HTTPResponse:
        pass

    def handle(self, msg):
        from_user_id = msg['FromUserName']
        to_user_id = msg['ToUserName']  # 接收人id
        other_user_id = msg['User']['UserName']  # 对手方id
        content = msg['Text']
        match_prefix = self.check_prefix(content, self.single_chat_prefix)
        if from_user_id == other_user_id and match_prefix is not None:
            # 好友向自己发送消息
            if match_prefix != '':
                str_list = content.split(match_prefix, 1)
                if len(str_list) == 2:
                    content = str_list[1].strip()

            img_match_prefix = self.check_prefix(content, self.image_create_prefix)
            if img_match_prefix:
                content = content.split(img_match_prefix, 1)[1].strip()
                self.thread_pool.submit(self._do_send_img, content, from_user_id)
            else:
                self.thread_pool.submit(self._do_send, content, from_user_id)

        elif to_user_id == other_user_id and match_prefix:
            # 自己给好友发送消息
            str_list = content.split(match_prefix, 1)
            if len(str_list) == 2:
                content = str_list[1].strip()
            img_match_prefix = self.check_prefix(content, self.image_create_prefix)
            if img_match_prefix:
                content = content.split(img_match_prefix, 1)[1].strip()
                self.thread_pool.submit(self._do_send_img, content, to_user_id)
            else:
                self.thread_pool.submit(self._do_send, content, to_user_id)

    def handle_group(self, msg):
        group_name = msg['User'].get('NickName', None)
        group_id = msg['User'].get('UserName', None)
        if not group_name:
            return ""
        origin_content = msg['Content']
        content = msg['Content']
        content_list = content.split(' ', 1)
        context_special_list = content.split('\u2005', 1)
        if len(context_special_list) == 2:
            content = context_special_list[1]
        elif len(content_list) == 2:
            content = content_list[1]

        match_prefix = (msg['IsAt'] and not self.group_at_off) or self.check_prefix(origin_content,
                                                                                    self.group_chat_prefix) \
                       or self.check_contain(origin_content, self.group_chat_keyword)
        if ('ALL_GROUP' in self.group_name_white_list or group_name in self.group_name_white_list or self.check_contain(
                group_name, self.group_name_keyword_white_list)) and match_prefix:
            img_match_prefix = self.check_prefix(content, self.image_create_prefix)
            if img_match_prefix:
                content = content.split(img_match_prefix, 1)[1].strip()
                self.thread_pool.submit(self._do_send_img, content, group_id)
            else:
                self.thread_pool.submit(self._do_send_group, content, msg)

    def send(self, msg, receiver):
        itchat.send(msg, toUserName=receiver)

    def _do_send(self, query, reply_user_id, reply_text):
        try:
            if not query:
                return
            context = dict()
            context['from_user_id'] = reply_user_id
            self.send(self.single_chat_reply_prefix + reply_text, reply_user_id)
        except Exception as e:
            logger.exception(e)

    def _do_send_img(self, query, reply_user_id, img_url):
        try:
            if not query:
                return
            context = dict()
            context['type'] = 'IMAGE_CREATE'
            if not img_url:
                return

            # 图片下载
            pic_res = requests.get(img_url, stream=True)
            image_storage = io.BytesIO()
            for block in pic_res.iter_content(1024):
                image_storage.write(block)
            image_storage.seek(0)

            # 图片发送
            logger.info('[WX] sendImage, receiver={}'.format(reply_user_id))
            itchat.send_image(image_storage, reply_user_id)
        except Exception as e:
            logger.exception(e)

    def _do_send_group(self, query, msg, reply_text):
        if not query:
            return
        context = dict()
        context['from_user_id'] = msg['ActualUserName']
        if reply_text:
            reply_text = '@' + msg['ActualNickName'] + ' ' + reply_text.strip()
            self.send(self.group_chat_reply_prefix + reply_text, msg['User']['UserName'])

    def check_prefix(self, content, prefix_list):
        for prefix in prefix_list:
            if content.startswith(prefix):
                return prefix
        return None

    def check_contain(self, content, keyword_list):
        if not keyword_list:
            return None
        for ky in keyword_list:
            if content.find(ky) != -1:
                return True
        return None
