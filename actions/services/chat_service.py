import json

import requests

from actions.constants.server_settings import server_settings


class ChatService:
    def __init__(self, app_url, app_key):
        self.app_key = app_key
        self.app_url = app_url

    def chat(self, sender_id, content):
        if server_settings.run_mode == 'debug':
            return '开发模式运行中.....'

        headers = {
            "Authorization": f"Bearer {self.app_key}",
            "Content-Type": "application/json",
        }
        data = {
            "chatId": sender_id,
            "stream": False,
            "detail": True,
            "messages": [
                {"content": content, "role": "user"}
            ],
        }
        response = requests.post(
            self.app_url,
            headers=headers,
            data=json.dumps(data),
            verify=False
        )
        response.raise_for_status()
        response_msg = response.json()["choices"][0]["message"]["content"]
        return response_msg
