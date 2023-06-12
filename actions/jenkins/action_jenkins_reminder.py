import datetime
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import (ReminderScheduled,
                             SlotSet, UserUtteranceReverted, FollowupAction, ActiveLoop)
from rasa_sdk.executor import CollectingDispatcher

from actions.constant.server_settings import server_settings
from actions.utils.core_utils import get_regex_entities
from actions.utils.jenkins_utils import (analyze_jenkins_build_console,
                                         get_jenkins_build_info,
                                         trigger_jenkins_pipeline, find_jenkins_job)


class ActionJenkinsReminder(Action):

    def name(self) -> Text:
        return "action_jenkins_reminder"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if server_settings.jenkins_url is None:
            dispatcher.utter_message('OpsPilot没有启用Jenkins自动化能力....')
            return []

        jenkins_pipeline_names = get_regex_entities(tracker, 'jenkins_pipeline_name')
        value = jenkins_pipeline_names[0]['value']
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
            SlotSet('jenkins_pipeline_name', None),
            SlotSet('jenkins_job_name', value),
            SlotSet('jenkins_job_buildnumber', build_number)
        ]
