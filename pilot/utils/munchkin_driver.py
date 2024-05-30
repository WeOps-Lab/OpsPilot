import json

import requests

from core.server_settings import server_settings


class MunchkinDriver:
    def chat(self, action_name, user_message, chat_history):
        chat_history = chat_history[:server_settings.chatgpt_model_max_history]
        result = requests.post(server_settings.munchkin_base_url + '/api/rag_search', data=json.dumps(
            {
                "bot_id": server_settings.munchkin_bot_id,
                "action_name": action_name,
                "user_message": user_message,
                "chat_history": chat_history
            }
        ), headers={
            "Authorization": f"TOKEN {server_settings.munchkin_api_key}",
            "Content-Type": "application/json"
        }).json()
        return result['result']
