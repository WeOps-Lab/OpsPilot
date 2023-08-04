from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionExecuteJob(Action):

    def name(self) -> Text:
        return "action_execute_job"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            f'目标IP:[{tracker.get_slot("ip_address")}],任务:{tracker.get_slot("internal_job_name")},执行完成，执行结果如下:....')
        return []
