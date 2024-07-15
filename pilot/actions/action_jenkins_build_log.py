from typing import Text, Any, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from eventbus.automation_eventbus import AutomationEventbus


class ActionJenkinsBuildLog(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_jenkins_build_log"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        eventbus = AutomationEventbus()
        eventbus.publish_automation_event("jenkins_build_log",
                                          tracker.sender_id, tracker.get_latest_input_channel(),
                                          params={
                                              "job_name": tracker.get_slot("jenkins_pipeline_name")
                                          })
        return [SlotSet("jenkins_pipeline_name", None)]
