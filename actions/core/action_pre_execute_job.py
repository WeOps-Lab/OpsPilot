from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.core_utils import get_regex_entities


class ActionPreExecuteJob(Action):

    def name(self) -> Text:
        return "action_pre_execute_job"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            f'开始执行任务:目标IP:[{tracker.get_slot("ip_address")}],任务:{tracker.get_slot("internal_job_name")},请稍后...')
        return []
