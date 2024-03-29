from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.constants.server_settings import server_settings
from actions.utils.jenkins_utils import JenkinsUtils


class ActionSearchJenkinsPipeline(Action):
    def name(self) -> Text:
        return "action_search_jenkins_pipeline"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        value = tracker.get_slot('search_jenkins_pipeline_name')
        jobs = JenkinsUtils().search_jenkins_job(value)
        if jobs is None:
            dispatcher.utter_message(f'没有找到名字包含[{value}]的流水线')
        else:
            message = f'找到名字包含[{value}]名称的流水线[{len(jobs)}]个，这里是我找到的流水线:'
            dispatcher.utter_message(text=message)

            for i in jobs:
                dispatcher.utter_message(text=i)
        return [SlotSet('search_jenkins_pipeline_name', None)]
