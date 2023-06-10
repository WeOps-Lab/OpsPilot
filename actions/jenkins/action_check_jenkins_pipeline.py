from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import (SlotSet, UserUtteranceReverted, FollowupAction, ActiveLoop)
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.core_utils import get_regex_entities
from actions.utils.jenkins_utils import (find_jenkins_job)


class ActionFindJenkinsPipeline(Action):
    def name(self) -> Text:
        return "action_check_jenkins_pipeline"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        jenkins_pipeline_names = get_regex_entities(tracker, 'jenkins_pipeline_name')
        if len(jenkins_pipeline_names) == 0:
            dispatcher.utter_message('没有识别到流水线的名称，示例：查看"demo"流水线')

        value = jenkins_pipeline_names[0]['value']
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
