import pickle
import faiss
import os
import re
import threading
import urllib.parse as urlparse
from dotenv import load_dotenv
from langchain import FAISS
import torch
import openai
import requests
from loguru import logger
from rasa_sdk.utils import read_yaml_file
from rasa.shared.constants import DEFAULT_CREDENTIALS_PATH
from rasa.core.channels.channel import UserMessage
from actions.utils.enterprise_wechat_utils import async_fun
from actions.utils.indexer_utils import Searcher
from actions.utils.langchain_utils import (
    langchain_qa,
    query_chatgpt,
    query_chatgpt_with_memory,
)
from actions.utils.redis_utils import RedisUtils, redis_client
from channels.WXBizMsgCrypt3 import WXBizMsgCrypt
import xml.etree.cElementTree as ET
from channels.enterprise_wechat_mysql import mysql_connect, mysql_select
from actions.constant.server_settings import server_settings
from langchain.embeddings import HuggingFaceEmbeddings

from channels.enterprise_wechat_utils import get_source_doc, helper_map_desc, struct_qywx_answer, text_split


class QYWXApp:
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

    def __init__(self, token, encoding_aes_key, corp_id, secret, agent_id):
        self.token = token
        self.encoding_aes_key = encoding_aes_key
        self.corp_id = corp_id
        self.secret = secret
        self.agent_id = agent_id
        self.access_token = self._get_access_token()

        self.km = self._get_km("km.pkl")

    def _get_km(self, pkl_name):
        """获取km标题链接字典，如没有则返回None

        Args:
            pkl_name (str): km标题链接字典序列化文件

        Returns:
            _type_: km标题链接字典
        """
        path = os.path.dirname(__file__)
        pkl_file = os.path.join(path, pkl_name)
        if pkl_name not in os.listdir(path):
            return None
        with open(pkl_file, "rb") as f:
            km = pickle.load(f)
        return km

    def _fresh_access_token(self):
        """刷新实例的access_token属性，便于后续接口调用"""
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
        if img_postfix == "":
            # dall-E返回的图片链接默认是png，且后缀不在链接尾
            img_postfix = "png"
        # 将png图片上传企微获得对应的media_id
        f = requests.get(img_url).content
        file = {"my_pic": ("pic_name", f, f"text/{img_postfix}")}
        request_params["method"] = "post"
        request_params["url"] = upload_url
        request_params["files"] = file
        res = self._requests_validate_expired(**request_params)
        return res["media_id"]

    def create_group(
        self, group_name: str, group_owner: str, group_user_list: list, chatid: str
    ) -> str:
        """通过企微应用创建企微应用群聊，返回群聊id

        Args:
            group_name (str): 群名称
            group_owner (str): 群主
            group_user_list (list): 群成员id列表
            chatid (str): 群聊的唯一标志，不能与已有的群重复；字符串类型，最长32个字符。只允许字符0-9及字母a-zA-Z。如果不填，系统会随机生成群id

        Returns:
            str: 群聊id，唯一标志群聊
        """

        setup_group_url = self.APPCHAT_CREATE.format(self.access_token)

        params = {
            "name": group_name,
            "owner": group_owner,
            "userlist": group_user_list,
            "chatid": chatid,
        }
        request_params = {"method": "post", "url": setup_group_url, "json": params}

        res = self._requests_validate_expired(**request_params)
        return res["chatid"]

    @async_fun
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
        assert msgtype in [
            "text",
            "image",
            "markdown",
        ], "目前OpsPilot版本仅支持发送文字(text,markdown)和图片(image)消息"
        assert (msgtype == "image" and media_id != "") or (
            msgtype == "text" or "markdown" and content != ""
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

        if msgtype == "text" or msgtype == "markdown":
            # 最长不超过2048个字节，对于长文本消息需要截断分多次发送
            content_list = text_split(content, 2048)
            for chunk in content_list:
                params[msgtype] = {"content": chunk}
                request_params = {"method": "post", "url": url, "json": params}
                res = self._requests_validate_expired(**request_params)
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

    @staticmethod
    def name_to_userid(name: str, seq: str = ";") -> list:
        """将用户名转换成对应的user_id
           首先需要：1.通过企微管理员从后台把通讯录导出；2.去把enterprise_wechat_mysql.py执行下

        Args:
            name (str): 企微用户姓名
            seq (str, optional): 姓名之间的分隔符，如果是单个姓名则没有. Defaults to ';'.

        Returns:
            list: 姓名对应的user_id列表
        """
        # 去掉姓名中带有的“(别名)”
        name = re.sub(r"\(.*?\)", "", name)

        name_or = "|".join(filter(None, name.split(seq)))
        select_sql = 'select user_id from qywx_contacts where name regexp "{}"'.format(
            name_or
        )

        db, cursor = mysql_connect()
        result = mysql_select(db, cursor, select_sql)
        if len(result) == 0:
            logger.error(f"未查询到用户名称对应的用户帐号，请检查传入的姓名{name}和分隔符{seq}")
        # 查询得到的是列表嵌套元组的形式
        result = [i[0] for i in result]
        return result

    def request_decrypt(self, request):
        """用经过企微服务器加密的用户对应用发送的消息进行解密

        Args:
            requset (request): request请求体

        Returns:
            user_id: 向应用发送消息的用户的企微帐号
            msg_type: 消息类型，进入应用为event，发送文本消息为text
            msg_content: 消息内容
        """
        # 企微应用消息解析
        query_args = dict(request.query_args)
        msg_signature = query_args["msg_signature"]
        timestamp = query_args["timestamp"]
        nonce = query_args["nonce"]
        data = request.body
        wxcpt = WXBizMsgCrypt(
            self.token,
            self.encoding_aes_key,
            self.corp_id,
        )
        _, msg = wxcpt.DecryptMsg(data, msg_signature, timestamp, nonce)
        xml_tree = ET.fromstring(msg)

        # 企微用户id
        user_id = xml_tree.find("FromUserName").text

        # 消息类型，event表示用户进入应用，text表示用户发送消息
        msg_type = xml_tree.find("MsgType").text
        msg_content = (
            xml_tree.find("Content").text
            if xml_tree.find("Content") is not None
            else None
        )
        logger.info(msg_content)

        return user_id, msg_type, msg_content

    @async_fun
    def post_dall_e_img(self, user_id, msg_content):
        """接收企微用户的dall 图片描述语句(msg_content)，发送openai接口返回的图片给到用户

        Args:
            user_id (_type_): 企微用户帐号
            msg_content (_type_): 图片描述语句
        """
        response = openai.Image.create(
            prompt=msg_content.strip("dall"),
            n=1,
            size="1024x1024",
            response_format="url",
        )
        image_url = response["data"][0]["url"]
        media_id = self._get_img_media_id(image_url)
        self.post_msg(user_id=user_id, msgtype="image", media_id=media_id)

    @async_fun
    def post_chatgpt_answer(self, user_id, msg_content):
        """接收企微用户的gpt 问题(msg_content)，发送openai接口返回的答案给到用户

        Args:
            user_id (str): 企微用户帐号
            msg_content (str): 企微用户问题
        """
        res = query_chatgpt_with_memory(
            user_id=user_id, query=msg_content.strip("gpt").strip()
        )
        # 如果res里含有<>格式，通过md格式发送，否则企微无法识别
        msg_type = "markdown" if re.findall("<.*>", res) else "text"
        self.post_msg(user_id=user_id, msgtype=msg_type, content=res)

    @staticmethod
    def init_qywx_km_index(km):
        """将键值形式的km标题形成faiss向量并进行文件持久化

        Args:
            pkl_path (_type_): 由知识库的标题（key）及对应超链接（value）组成
        """
        sentence_embeddings = torch.Tensor(embeddings.embed_documents(list(km.keys())))
        dimension = sentence_embeddings.shape[1]
        # 数据量不大，使用平面索引，如果量过大，考虑采用分区索引和量化索引
        index = faiss.IndexFlatL2(dimension)
        index.add(sentence_embeddings)
        faiss.write_index(
            index, os.path.join(os.path.dirname(__file__), "km_question.index")
        )

    def km_qa(self, query, top_n=10):
        """根据query搜索最相似的N个km标题及对应链接

        Args:
            query (str): 问题
            km (dict, optional): 标题链接映射. Defaults to None.
            top_n (int, optional): 返回前n个相似. Defaults to 10.

        Returns:
            _type_: _description_
        """

        path = os.path.dirname(__file__)

        if "km_question.index" not in os.listdir(path):
            QYWXApp.init_qywx_km_index(self.km)

        index = faiss.read_index(os.path.join(path, "km_question.index"))
        search = torch.Tensor(embeddings.embed_documents([query]))
        D, I = index.search(search, top_n)
        sim_query = [list(self.km.keys())[i] for i in I[0]]
        link = [self.km[k] for k in sim_query]
        return sim_query, link

    @async_fun
    def qywx_km_qa(self, user_id, query, top_n=10):
        """根据langchainQA返回基于本地知识的回答并结合问题相似度返回最相似的n个km标题链接

        Args:
            user_id (str): 企微用户id
            query (str): 企微用户要检索的km内容
        """

        # 1.返回langchain_qa的答案，并附加上其来源链接
        prompt_template = RedisUtils.get_prompt_template()
        prompt_template = searcher.format_prompt(prompt_template, query)
        results = langchain_qa(doc_search, prompt_template, query)
        # 2.将答案的来源链接添加到km标题的排序里面
        langchain_source = dict(
            map(
                lambda x: get_source_doc(x.metadata["source"], self.km),
                results["source_documents"],
            )
        )
        # 4.对参考链接排序
        langchain_prefix = "\n本回答来源如下："
        title_sim_prefix = "\n根据您的问题，您还可以查看以下结果："
        sim_query, link = self.km_qa(query, top_n=top_n)
        sim_query_dict = dict(zip(sim_query, link))

        sim_query_dict = dict(
            set(sim_query_dict.items()) - set(langchain_source.items())
        )
        sim_query_dict = dict(list(sim_query_dict.items())[:5])
        result = (
            results["result"]
            + langchain_prefix
            + struct_qywx_answer(
                len(langchain_source),
                list(langchain_source.values()),
                list(langchain_source.keys()),
            )
            + title_sim_prefix
            + struct_qywx_answer(
                len(sim_query_dict),
                list(sim_query_dict.values()),
                list(sim_query_dict.keys()),
            )
        )

        # 3.若本地未匹配到相关文档，当前通过正则匹配，后续考虑意图识别
        negative_rule = re.compile(r"无法回答|不知道|没有.*信息|未提供.*信息|无关|不确定|没有提到")
        if re.findall(negative_rule, results["result"]):
            # 转为gpt问答
            system_message = "Answer as detailed as possible and use Chinese to answer."
            gpt_answer = query_chatgpt(
                system_message=system_message, user_message=query
            )
            result = result.replace(langchain_prefix, "\n可以参考如下来源：").replace(
                results["result"], gpt_answer
            )
            result = "您的问题没有在本地知识库检索到，下面是gpt的回答：\n" + result
        self.post_msg(user_id=user_id, content=result)
        # redis记录用户问题，供helper功能使用，保存10分钟
        redis_client.rpush("km_" + user_id, query)
        redis_client.expire("km_" + user_id, 10*60)
        # 发送提示，告知用户序号对应的helper，每天一次
        if redis_client.get("km_helper" + user_id):
            return
        redis_client.set("km_helper" + user_id, "km_helper", ex=24 * 60 * 60)
        self.post_msg(user_id=user_id, content=helper_map_desc())
        

    @async_fun
    def post_funny_msg(self, user_id):
        """调用接口，每人每天返回一句精美句子

        Args:
            user_id (str): 企微用户ID
        """
        if redis_client.get("hitokoto" + user_id):
            return
        redis_client.set("hitokoto" + user_id, "hi", ex=24 * 60 * 60)
        netease_comment_url = "https://v1.hitokoto.cn/"
        try:
            hitokoto = requests.get(netease_comment_url).json()["hitokoto"]
        except Exception as e:
            logger.exception("调用热评接口出错：{e}")
            return
        self.post_msg(user_id=user_id, content="每日一句：" + hitokoto)

    async def qywx_rasa_qa(
        self, request, user_id, msg_content, collector, input_channel
    ):
        await request.app.ctx.agent.handle_message(
            UserMessage(
                text=msg_content,
                output_channel=collector,
                sender_id=user_id,
                input_channel=input_channel,
                metadata=None,
            )
        )
        response_data = collector.messages
        res_content = (
            "\n\n".join(data["text"] for data in response_data)
            .replace("bot:", "")
            .replace(server_settings.default_thinking_message, "")
            .strip()
        )
        self.post_msg(user_id=user_id, msgtype="text", content=res_content)
    
    @async_fun
    def judge_create_helper_group(self, user_id, msg_content):
        # 获取helper信息
        try:
            helper_info = list(filter(lambda x: "HELPER" in x[0] and msg_content in x[0], os.environ.items()))[0]
            helper_name = helper_info[0]
            helper_owner = helper_info[1]
        except Exception as e:
            logger.exception('请检查是否有正确配置helper环境变量')
            raise e
        helper_chat_id = helper_name.replace("_", "")
        # 创建群聊 or 将用户拉入群聊
        res_get_chat = self.get_group(chatid=helper_chat_id)
        if res_get_chat is None:
            # 说明未创建此群聊，需要通过接口创建群聊，并手动拉入对应Helper
            self.create_group(
                helper_name[:-2],
                group_owner=helper_owner,
                group_user_list=[helper_owner, user_id],
                chatid=helper_chat_id,
            )
        else:
            self.update_group(chatid=helper_chat_id, add_user_list=[user_id])
        # 发送历史km问题
        for i in range(redis_client.llen("km_" + user_id)):
            chat_msg = redis_client.lindex("km_" + user_id, i)
            self.post_msg(chatid=helper_chat_id, content=chat_msg)
         # 30分钟后自动踢出群聊
        t1 = threading.Timer(30*60, self.update_group, kwargs={'chatid':helper_chat_id, 'del_user_list':[user_id]})
        # 启动线程
        t1.start()


load_dotenv()
RUN_MODE = os.getenv("RUN_MODE")
credentials_path = (
    "dev-config/credentials.yml" if RUN_MODE == "DEV" else DEFAULT_CREDENTIALS_PATH
)
credentials = read_yaml_file(credentials_path)
qywx_app = QYWXApp(
    **credentials["channels.enterprise_wechat_channel.EnterpriseWechatChannel"]
)

embeddings = HuggingFaceEmbeddings(
    model_name=server_settings.embed_model_name,
    cache_folder=server_settings.embed_model_cache_home,
    encode_kwargs={"show_progress_bar": True},
)
doc_search = FAISS.load_local(server_settings.vec_db_path, embeddings)
searcher = Searcher()
