import os
import urllib.parse as urlparse
import requests
from loguru import logger

from channels.enterprise_wechat_channel import EnterpriseWechatChannel


class QYWXApp():
    """
    企业微信应用，支持：
    1.创建群聊
    2.获取群聊详情
    3.更新（删除）群聊
    4.群消息（文本、图片类型）发送
    5.个人消息（文本、图片类型）发送
    PS.统一了API请求出口和access_token过期处理方式，后续企微API统一于此类更新
    """

    BASE_URL = "https://qyapi.weixin.qq.com"

    GET_ACCESS_TOKEN = BASE_URL + "/cgi-bin/gettoken?corpid={}&corpsecret={}"
    USER_MESSAGE_SEND = BASE_URL + "/cgi-bin/message/send?access_token={}"
    APPCHAT_CREATE = BASE_URL + "/cgi-bin/appchat/create?access_token={}"
    APPCHAT_SEND = BASE_URL + "/cgi-bin/appchat/send?access_token={}"
    APPCHAT_GET = BASE_URL + "/cgi-bin/appchat/get?access_token={}&chatid={}"
    APPCHAT_UPDATE = BASE_URL + "/cgi-bin/appchat/update?access_token={}"
    MEDIA_UPLOAD = BASE_URL + "/cgi-bin/media/upload?access_token={}&type={}"

    def __init__(
        self, token, encoding_aes_key, corp_id, secret, agent_id
    ):
        self.token = token
        self.encoding_aes_k=encoding_aes_key
        self.corp_id = corp_id
        self.secret = secret
        self.token = agent_id
        self.access_token = self._get_access_token()

    def _fresh_access_token(self):
        """刷新实例的access_token属性，便于后续接口调用
        """
        self.access_token = self._get_access_token()

    def _requests_validate_expired(self, **request_params):
        """API统一请求，关键字参数包括请求方式、url、参数等

        Returns:
            dict: 企业微信接口返回体
        """
        res = requests.request(**request_params).json()
        if res.get("errcode") == 0:
            return res
        elif res.get("errcode") == 40014 or res.get("errcode") == 42001:
            self._fresh_access_token()
            old_access_token = urlparse.parse_qs(
                urlparse.urlparse(request_params["url"]).query
            )["access_token"][0]
            request_params["url"] = request_params["url"].replace(
                old_access_token, self.access_token
            )
            res_again = requests.request(**request_params).json()
            if res_again.get("errcode") != 0:
                logger.exception(f"access_token已刷新，但接口调用仍失败，返回结果:{res}")
            return res_again
        else:
            logger.exception(f"接口调用失败，返回结果:{res}")

    def _get_access_token(self):
        """获取最新的access_token

        Returns:
            str: access_token
        """
        url = self.GET_ACCESS_TOKEN.format(self.corp_id, self.secret)
        res = requests.get(url).json()
        if res.get("errcode") == 0:
            return res["access_token"]
        else:
            logger.exception(f"无法获取token，原因：{res}")

    def _get_img_media_id(self, img_url):
        """应用发送图片之前需要先将图片上传至企微服务器，并获取媒体id

        Args:
            img_url (str): 图片的图床地址

        Returns:
            str: media_id
        """
        # 这里考虑到一键建群发送的图片来自于工单、wiki，因此默认用的是图床的URL
        # 本地图片和base64尚不支持
        upload_url = self.MEDIA_UPLOAD.format(self.access_token, "image")

        request_params = dict()
        img_postfix = os.path.splitext(img_url)[-1][1:]
        # 将png图片上传企微获得对应的media_id
        f = requests.get(img_url).content
        file = {"my_pic": ("pic_name", f, f"text/{img_postfix}")}
        request_params["method"] = "post"
        request_params["url"] = upload_url
        request_params["files"] = file
        res = self._requests_validate_expired(**request_params)
        return res["media_id"]

    def create_group(
        self,
        group_name: str,
        group_owner: str,
        group_user_list: list,
    ) -> str:
        """通过企微应用创建企微应用群聊，返回群聊id

        Args:
            group_name (str): 群名称
            group_owner (str): 群主
            group_user_list (list): 群成员列表

        Returns:
            str: 群聊id，唯一标志群聊
        """

        setup_group_url = self.APPCHAT_CREATE.format(self.access_token)

        params = {"name": group_name, "owner": group_owner, "userlist": group_user_list}
        request_params = {"method": "post", "url": setup_group_url, "json": params}

        res = self._requests_validate_expired(**request_params)
        return res["chatid"]

    def post_msg(
        self,
        chatid: str = "",
        user_id: str = "",
        msgtype: str = "text",
        content: str = "",
        media_id: str = "",
    ):
        """通过企微应用发送消息（文字、图片）给企微群聊或用户

        Args:
            chatid (str, optional): 群id. Defaults to "".
            user_id (str, optional): 用户id. Defaults to "".
            msgtype (str, optional): 消息类型. Defaults to "text".
            content (str, optional): 消息文本内容. Defaults to "".
            media_id (str, optional): 消息媒体id. Defaults to "".

        Returns:
            dict: 企微接口返回体
        """
        assert msgtype in ["text", "image"], "目前OpsPilot版本仅支持发送文字(text)和图片(image)消息"
        assert (msgtype == "image" and media_id != "") or (
            msgtype == "text" and content != ""
        ), "发送图片/文字消息，缺失必要参数"
        params = dict()
        if chatid != "":
            # 说明是发送群聊消息
            url = self.APPCHAT_SEND.format(self.access_token)
            params["chatid"] = chatid
            params["msgtype"] = msgtype
        else:
            # 说明是发送用户消息
            params["msgtype"] = msgtype
            params["touser"] = user_id
            params["agentid"] = self.agent_id
            params["safe"] = 0
            params["duplicate_check_interval"] = 1800
            url = self.USER_MESSAGE_SEND.format(self.access_token)

        if msgtype == "text":
            # 发送的是文本消息
            # 最长不超过2048个字节，对于长文本消息需要截断分多次发送
            params["text"] = {"content": content}
        if msgtype == "image":
            # 发送的是图片消息
            params["image"] = {"media_id": media_id}

        request_params = {"method": "post", "url": url, "json": params}
        res = self._requests_validate_expired(**request_params)
        return res

    def get_group(
        self,
        chatid: str,
    ):
        """获取群聊信息，包括群名，群主，群成员列表等

        Args:
            chatid (str): 群聊ID
        """
        get_group_url = self.APPCHAT_GET.format(self.access_token, chatid)
        request_params = {"method": "get", "url": get_group_url}

        res = self._requests_validate_expired(**request_params)
        return res

    def update_group(
        self,
        chatid: str,
        group_name: str = None,
        group_owner: str = None,
        add_user_list: list = [],
        del_user_list: list = [],
    ):
        """更新群（包括删除）

        Args:
            chatid (str): 群聊ID
            group_name (str): 更改后的群名，默认不更改，Defaults to None.
            group_owner (str, optional): 更改后的群名，默认不更改. Defaults to None.
            add_user_list (list, optional): 要新增的群成员列表. Defaults to [].
            del_user_list (list, optional): 要从当前群聊中删除的群成员列表. Defaults to [].
        """
        update_group_url = self.APPCHAT_UPDATE.format(self.access_token)

        params = {
            "chatid": chatid,
            "name": group_name,
            "owner": group_owner,
            "add_user_list": add_user_list,
            "del_user_list": del_user_list,
        }
        request_params = {"method": "post", "url": update_group_url, "json": params}

        res = self._requests_validate_expired(**request_params)
        return res
