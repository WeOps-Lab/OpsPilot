import json
from typing import Text, Any, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from utils.eventbus import EventBus, AUTOMATION_EVENT
from utils.munchkin_driver import MunchkinDriver


class ActionListJenkinsJobs(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_list_jenkins_jobs"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        event = {
            "event_type": AUTOMATION_EVENT,
            "automation_event": "list_jenkins_jobs",
            "sender_id": tracker.sender_id,
            "channel": tracker.get_latest_input_channel()
        }
        eventbus = EventBus()
        eventbus.publish(json.dumps(event))
