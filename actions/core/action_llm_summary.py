import datetime
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.executor import CollectingDispatcher

from actions.constants.server_settings import server_settings
from actions.services.chat_service import ChatService


class ActionLlmSummary(Action):
    def __init__(self):
        self.chat_service = ChatService(server_settings.fastgpt_content_summary_key)

    def name(self) -> Text:
        return "action_llm_summary"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if self.chat_service.has_llm_backend() is False:
            dispatcher.utter_message('OpsPilot没有启用LLM能力....')
            return []

        events = list(
            filter(
                lambda x: x.get("event") == "user"
                          or x.get("event") == "bot",
                tracker.events,
            )
        )
        user_messages = []
        for event in reversed(events):
            if len(user_messages) >= server_settings.chatgpt_model_max_history:
                break
            user_messages.insert(0, event)
        user_prompt = ""
        for user_message in user_messages:
            user_prompt += f"{user_message['text']}\n"
        response_msg = self.chat_service.chat(tracker.sender_id, user_prompt)

        logger.info(f"[对话总结]用户的对话记录: {user_prompt},总结的内容: {response_msg}")
        dispatcher.utter_message(response_msg)
        return []
