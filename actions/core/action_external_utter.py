from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionExternalUtter(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_external_utter"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities')
        content = next(
            (x['value'] for x in entities if x['entity'] == 'content'),
            None
        )
        dispatcher.utter_message(content)
