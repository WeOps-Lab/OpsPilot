from typing import Text, Any, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionOnlineSearch(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_online_search"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="已经为您开启联网搜索,使用结束后，可以使用`/reset`重置状态")
        return [SlotSet("enable_online_search", True)]
