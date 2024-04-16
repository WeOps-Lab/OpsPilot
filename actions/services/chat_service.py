import json

import requests

from actions.constants.server_settings import server_settings


class ChatService:

    def has_llm_backend(self):
        return server_settings.fastgpt_endpoint is not None

    def chat(self, sender_id, content):
        headers = {
            "Authorization": f"Bearer {server_settings.fastgpt_key}",
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
            server_settings.fastgpt_endpoint,
            headers=headers,
            data=json.dumps(data),
        )
        response.raise_for_status()
        response_msg = response.json()["choices"][0]["message"]["content"]
        return response_msg
