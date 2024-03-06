from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import (SlotSet, UserUtteranceReverted, FollowupAction, ActiveLoop)
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.jenkins_utils import JenkinsUtils


class ActionFindJenkinsPipeline(Action):
    def name(self) -> Text:
        return "action_check_jenkins_pipeline"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        jenkins_utils = JenkinsUtils()
        value = tracker.get_slot('build_jenkins_pipeline_name')
        if len(value) == 0:
            dispatcher.utter_message(f'没有找到[{value}]流水线')

        dispatcher.utter_message(f"检查[{value}]流水线是否存在......")

        job_exist = jenkins_utils.find_jenkins_job(value)
        if job_exist:
            logger.info(f'流水线[{value}]存在，继续执行后续任务')
            return []
        else:
            dispatcher.utter_message(f"没有找到[{value}]流水线")
            # jobs = jenkins_utils.search_jenkins_job(value)
            # if len(jobs) != 0:
            #     buttons = []
            #     for job in jobs:
            #         buttons.append({
            #             "title": job,
            #             "payload": f"/build_jenkins_pipeline{{\"build_jenkins_pipeline_name\":\"{job}\"}}"
            #         })
            #     dispatcher.utter_button_message('找到以下比较相似的流水线', buttons)
            return [
                UserUtteranceReverted(),
            ]
