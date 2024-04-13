from actions.constants.server_settings import server_settings
from actions.services.dify_service import DifyService
from actions.services.fastgpt_service import FastGptService


class ChatService:
    def __init__(self):
        self.dify_service = DifyService(server_settings.dify_endpoint, server_settings.dify_key)
        self.fastgpt_service = FastGptService(server_settings.fastgpt_endpoint, server_settings.fastgpt_key)

    def chat(self, sender_id, content):
        if server_settings.fallback_llm == "FAST_GPT":
            response_msg = self.fastgpt_service.chat(sender_id, content)
            return response_msg
        else:
            response_msg = self.dify_service.chat(server_settings.dify_endpoint, server_settings.dify_key,
                                                  sender_id,
                                                  content)
            return response_msg
