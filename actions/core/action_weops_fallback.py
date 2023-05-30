from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset, UserUtteranceReverted, ConversationPaused, Restarted, ActionReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.azure_utils import query_chatgpt


class ActionWeOpsFallback(Action):

    def name(self) -> Text:
        return "action_weops_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(tracker.latest_message['text'])
        if tracker.active_loop_name is None:
            dispatcher.utter_message(text='WeOps正在思考中........')
            result = query_chatgpt([
                {"role": "user", "content": tracker.latest_message['text']},
            ])
            dispatcher.utter_message(text=result)
            return [UserUtteranceReverted()]
        else:
            print("FallBack")
            return []
