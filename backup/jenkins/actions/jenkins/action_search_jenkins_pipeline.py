from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import (SlotSet, UserUtteranceReverted, FollowupAction, ActiveLoop)
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.jenkins_utils import (find_jenkins_job, search_jenkins_job)


class ActionSearchJenkinsPipeline(Action):
    def name(self) -> Text:
        return "action_search_jenkins_pipeline"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        jenkins_pipeline_name = tracker.get_slot('jenkins_pipeline_name')
        jobs = search_jenkins_job(jenkins_pipeline_name)
        if jobs is None:
            dispatcher.utter_message(f'没有找到名字包含[{jenkins_pipeline_name}]的流水线')
        else:
            message = f'找到名字包含[{jenkins_pipeline_name}]名称的流水线[{len(jobs)}]个，这里是我找到的流水线:'
            dispatcher.utter_message(text=message)
            for i in jobs:
                dispatcher.utter_message(text=i)
        return []
