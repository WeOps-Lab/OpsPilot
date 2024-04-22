from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.constants.server_settings import server_settings
from actions.services.chat_service import ChatService
from utils.core_logger import log_info
from utils.rasa_utils import load_chat_history


class ActionLlmSummary(Action):
    def __init__(self):
        self.chat_service = ChatService(server_settings.fastgpt_endpoint, server_settings.fastgpt_content_summary_key)

    def name(self) -> Text:
        return "action_llm_summary"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        user_message = load_chat_history(tracker, server_settings.chatgpt_model_max_history)
        response_msg = self.chat_service.chat(tracker.sender_id, user_message)
        log_info(tracker, f"[对话总结]用户的对话记录: {user_message},总结的内容: {response_msg}")

        dispatcher.utter_message(response_msg)
        return []
