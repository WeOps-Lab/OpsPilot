import datetime
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import (ReminderScheduled,
                             SlotSet, UserUtteranceReverted, FollowupAction, ActiveLoop)
from rasa_sdk.executor import CollectingDispatcher

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
        jenkins_pipeline_name = tracker.get_slot('jenkins_pipeline_name')
        dispatcher.utter_message(f"流水线[{jenkins_pipeline_name}]开始构建,任务正在排队构建......")
        build_number = trigger_jenkins_pipeline(jenkins_pipeline_name)

        dispatcher.utter_message(
            f"流水线[{jenkins_pipeline_name}]开始构建,构建号为:[{build_number}],任务构建完成后WeOps会通知你,请耐心等待......"
        )

        date = datetime.datetime.now() + datetime.timedelta(seconds=5)
        reminder = ReminderScheduled(
            "EXTERNAL_jenkins_reminder",
            trigger_date_time=date,
            entities={
                "build_number": build_number,
                "job_name": jenkins_pipeline_name
            },
            name='jenkins_reminder',
            kill_on_user_message=False,
        )

        return [
            reminder,
            SlotSet('jenkins_pipeline_name', None),
            SlotSet('jenkins_job_name', jenkins_pipeline_name),
            SlotSet('jenkins_job_buildnumber', build_number)
        ]
