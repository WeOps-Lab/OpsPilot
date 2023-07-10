import json
import requests

from actions.constant.server_settings import server_settings

ACCESS_TOKEN = server_settings.access_token


def get_access_token():
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={server_settings.corp_id}&corpsecret={server_settings.secret}"
    access_token = json.loads(requests.get(url).content)["access_token"]
    print(access_token)
    return access_token


def post_message(user_id, content):
    """
    description: 企微应用通过接口发送消息给企微用户
    """

    global ACCESS_TOKEN

    params = {
        "touser": user_id,
        "msgtype": "text",
        "agentid": server_settings.agent_id,
        "text": {"content": content},
        "safe": 0,
        "duplicate_check_interval": 1800,
    }
    if server_settings.access_token == "":
        ACCESS_TOKEN = get_access_token()
    post_msg_url = (
        f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={ACCESS_TOKEN}"
    )
    res = json.loads(requests.post(url=post_msg_url, data=json.dumps(params)).content)
    if res["errcode"] != 0:
        # 出现如下错误码说明说明token过期，重新获取token并发送消息
        if res["errcode"] == 40014 or res["errcode"] == 42001:
            ACCESS_TOKEN = get_access_token()
            post_msg_url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={ACCESS_TOKEN}"
            res = json.loads(
                requests.post(url=post_msg_url, data=json.dumps(params)).content
            )
            # 再次出错，说明不是token的问题，需要深入排查
            if res["errcode"] != 0:
                print("重新获取ACCESS_TOKEN后发送消息失败，res为:", res)
        if res["errcode"] == 60020:
            print(f"IP不是可信IP，详细信息：{res}")
