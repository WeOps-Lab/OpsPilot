import requests


class EnterpriseWechatBot:
    @staticmethod
    def send_message(url: str, content: str):
        """
        发送企业微信机器人文本消息
        :param url:
        :param content:
        :return:
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        response = requests.post(url, headers={
            'Content-Type': 'application/json'
        }, json=data)

        return response.json()
