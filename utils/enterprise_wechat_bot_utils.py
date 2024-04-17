import requests


class EnterpriseWechatBotUtils:
    @staticmethod
    def send_wechat_notification(url, content):
        headers = {'Content-Type': 'application/json'}
        data = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        response = requests.post(url, headers=headers, json=data, verify=False)
        return response.json()
