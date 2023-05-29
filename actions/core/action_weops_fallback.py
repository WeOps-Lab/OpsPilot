from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset, UserUtteranceReverted, ConversationPaused, Restarted, ActionReverted
from rasa_sdk.executor import CollectingDispatcher


class ActionWeOpsFallback(Action):

    def name(self) -> Text:
        return "action_weops_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message['text'])
        if tracker.active_loop_name is None:
            # result = query_chatgpt(tracker.latest_message['text'])
            dispatcher.utter_message(text='WeOps正在思考中........')
            dispatcher.utter_message(text="WeOps FallBack")
            return [UserUtteranceReverted()]
        else:
            print("FallBack")
            return []
