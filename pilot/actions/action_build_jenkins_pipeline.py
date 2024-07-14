from typing import Text, Any, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from eventbus.automation_eventbus import AutomationEventbus


class ActionBuildJenkinsPipeline(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_build_jenkins_pipeline"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        eventbus = AutomationEventbus()
        eventbus.publish("build_jenkins_pipeline",
                         tracker.sender_id,
                         tracker.get_latest_input_channel())
