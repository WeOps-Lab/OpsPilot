from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionRebootServer(Action):

    def name(self) -> Text:
        return "action_reboot_server"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reboot_server = tracker.get_slot("reboot_server")
        dispatcher.utter_message(f'重启服务器[{reboot_server}]......')
        return []