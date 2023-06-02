from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import (ActiveLoop, FollowupAction, SlotSet, UserUtteranceReverted)
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.jenkins_utils import (find_jenkins_job)


class ActionFindJenkinsPipeline(Action):
    def name(self) -> Text:
        return "action_find_jenkins_pipeline"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        jenkins_pipeline_name = tracker.get_slot('jenkins_pipeline_name')
        dispatcher.utter_message(f"检查[{jenkins_pipeline_name}]流水线是否存在......")

        job_exist = find_jenkins_job(jenkins_pipeline_name)
        if job_exist:
            logger.info(f'流水线[{jenkins_pipeline_name}]存在，继续执行后续任务')
            return []
        else:
            dispatcher.utter_message(f"没有找到[{jenkins_pipeline_name}]流水线,请重新输入流水线名称")

            return [
                SlotSet('jenkins_pipeline_name', None),
                SlotSet('jenkins_job_name', None),
                SlotSet('jenkins_job_buildnumber', None),
                SlotSet('requested_slot', 'jenkins_pipeline_name'),
                UserUtteranceReverted(),
                FollowupAction('jenkins_pipeline_form'),
                ActiveLoop('jenkins_pipeline_form'),
            ]

