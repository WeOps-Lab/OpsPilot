from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.constant.server_settings import server_settings
from actions.utils.langchain_utils import query_online


class ActionOnlineChat(Action):

    def name(self) -> Text:
        return "action_online_chat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if server_settings.enable_online_chat:
            dispatcher.utter_message('开始进行联网学习,请稍后......')
            online_chat_url = tracker.get_slot('online_chat_url')
            online_chat_query = tracker.get_slot('online_chat_query')
            results = query_online(online_chat_url, online_chat_query)
            dispatcher.utter_message(results)
        else:
            dispatcher.utter_message('OpsPilot没有启用联网学习的能力,无法完成联网知识问答哦')
        return [SlotSet('online_chat_url', None), SlotSet('online_chat_query', None), ]
