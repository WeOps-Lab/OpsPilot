from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions import server_settings


class ActionWeOpsPreFallback(Action):

    def name(self) -> Text:
        return "action_pre_weops_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message['text']
        if user_msg != '':
            dispatcher.utter_message(text=server_settings.default_thinking_message)

        return []
