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
            self.app_url + '/api/v1/chat/completions',
            headers=headers,
            data=json.dumps(data),
            # verify=False
        )
        response.raise_for_status()

        result_data = response.json()
        response_msg = result_data["choices"][0]["message"]["content"]
        if server_settings.enable_llm_source_detail:
            try:
                doc_source = set()
                for source in response.json()['responseData'][0]['quoteList']:
                    doc_source.add(source['sourceName'])
                response_msg += '\n知识来源：\n'
                for index, source in enumerate(doc_source):
                    response_msg += f'{index + 1}: {source}\n'
            except:
                pass
        return response_msg
