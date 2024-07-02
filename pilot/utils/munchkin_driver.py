import json

import requests

from core.server_settings import server_settings


class MunchkinDriver:
    def salt_local_execute(self, salt_params, sender_id=''):
        result = requests.post(server_settings.munchkin_base_url + '/api/bot/salt_execute', data=json.dumps(
            {
                "bot_id": server_settings.munchkin_bot_id,
                "params": salt_params,
                "sender_id": sender_id
            }
        ), headers={
            "Authorization": f"TOKEN {server_settings.munchkin_api_key}",
            "Content-Type": "application/json"
        }).json()
        return result['result']['return'][0]['ops-pilot']

    def chat(self, action_name, user_message, chat_history, sender_id=''):
        chat_history = chat_history[:server_settings.chatgpt_model_max_history]
        result = requests.post(server_settings.munchkin_base_url + '/api/bot/skill_execute', data=json.dumps(
            {
                "bot_id": server_settings.munchkin_bot_id,
                "skill_id": action_name,
                "sender_id": sender_id,
                "user_message": user_message,
                "chat_history": chat_history
            }
        ), headers={
            "Authorization": f"TOKEN {server_settings.munchkin_api_key}",
            "Content-Type": "application/json"
        }).json()
        return result['result']
