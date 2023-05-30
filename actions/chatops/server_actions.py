from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionRebootServer(Action):

    def name(self) -> Text:
        return "action_reboot_server"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        reboot_server = tracker.get_slot("reboot_server")
        if tracker.latest_message['intent']['name'] == 'affirm':
            dispatcher.utter_message(f'重启服务器[{reboot_server}]......')
        if tracker.latest_message['intent']['name'] == 'deny':
            dispatcher.utter_message(f'取消重启服务器[{reboot_server}]')
        return [SlotSet('reboot_server', None)]
