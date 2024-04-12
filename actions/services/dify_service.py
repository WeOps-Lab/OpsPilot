import json

import requests
from rasa_sdk import logger


class DifyService:
    def __init__(self, dify_endpoint, dify_key):
        self.dify_endpoint = dify_endpoint
        self.dify_key = dify_key

    def chat(self, user_id, message):
        headers = {
            "Authorization": f"Bearer {self.dify_key}",
            "Content-Type": "application/json",
        }

        data = {
            "inputs": {},
            "query": message,
            "response_mode": "streaming",
            "conversation_id": "",
            "user": user_id
        }

        response = requests.post(self.dify_endpoint, headers=headers, json=data, stream=True)
        response.raise_for_status()

        response_msg = ""
        for line in response.iter_lines():
            if line:
                json_data = json.loads(line.decode('utf-8')[5:])
                if 'answer' in json_data:
                    response_msg += json_data['answer']
        return response_msg
