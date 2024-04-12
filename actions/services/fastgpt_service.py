import json

import requests


class FastGptService:
    def __init__(self, fastgpt_endpoint, fastgpt_key):
        self.fastgpt_endpoint = fastgpt_endpoint
        self.fastgpt_key = fastgpt_key

    def chat(self, sender_id, content):
        headers = {
            "Authorization": f"Bearer {self.fastgpt_key}",
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
            self.fastgpt_endpoint,
            headers=headers,
            data=json.dumps(data),
        )
        response_msg = response.json()["choices"][0]["message"]["content"]
        return response_msg
