import datetime
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import (ReminderScheduled,
                             SlotSet)
from rasa_sdk.executor import CollectingDispatcher

from actions.constant.server_settings import server_settings
from actions.utils.jenkins_utils import (trigger_jenkins_pipeline)


class ActionBuildJenkinsPipeline(Action):

    def name(self) -> Text:
        return "action_build_jenkins_pipeline"

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
        dispatcher.utter_message(f"流水线[{value}]开始构建,任务正在排队构建......")
        build_number = trigger_jenkins_pipeline(value)

        dispatcher.utter_message(
            f"流水线[{value}]开始构建,构建号为:[{build_number}],任务构建完成后WeOps会通知你,请耐心等待......"
        )

        date = datetime.datetime.now() + datetime.timedelta(seconds=5)
        reminder = ReminderScheduled(
            "EXTERNAL_jenkins_reminder",
            trigger_date_time=date,
            entities={
                "build_number": build_number,
                "job_name": value
            },
            name='jenkins_reminder',
            kill_on_user_message=False,
        )

        return [
            reminder,
            SlotSet('build_jenkins_pipeline_name', None),
            SlotSet('jenkins_job_name', value),
            SlotSet('jenkins_job_buildnumber', build_number)
        ]
