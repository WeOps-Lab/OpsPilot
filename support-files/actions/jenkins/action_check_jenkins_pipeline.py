from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.constants.server_settings import server_settings
from actions.jenkins.jenkins_utils import find_jenkins_job


class ActionFindJenkinsPipeline(Action):
    def name(self) -> Text:
        return "action_check_jenkins_pipeline"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if server_settings.enable_jenkins_skill is False:
            dispatcher.utter_message('OpsPilot没有启用Jenkins自动化能力....')
            return []

        value = tracker.get_slot('build_jenkins_pipeline_name')
        if len(value) == 0:
            dispatcher.utter_message(f'没有找到[{value}]流水线')

        dispatcher.utter_message(f"检查[{value}]流水线是否存在......")

        job_exist = find_jenkins_job(value)
        if job_exist:
            logger.info(f'流水线[{value}]存在，继续执行后续任务')
            return []
        else:
            dispatcher.utter_message(f"没有找到[{value}]流水线")

            return [
                UserUtteranceReverted(),
            ]
