import datetime
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import (ActiveLoop, FollowupAction, ReminderScheduled,
                             SlotSet, UserUtteranceReverted)
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.jenkins_utils import (analyze_jenkins_build_console,
                                         find_jenkins_job,
                                         get_jenkins_build_info,
                                         trigger_jenkins_pipeline)


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
        dispatcher.utter_message(f"查找[{jenkins_pipeline_name}]流水线")
        job_exist = find_jenkins_job(jenkins_pipeline_name)
        if job_exist:
            return []
        else:
            dispatcher.utter_message(f"没有找到[{jenkins_pipeline_name}]流水线,请重新输入流水线名称")

            return [
                UserUtteranceReverted(),
                FollowupAction('jenkins_pipeline_form'),
                ActiveLoop('jenkins_pipeline_form'),
                SlotSet('jenkins_pipeline_name', None),
                SlotSet('jenkins_job_name', None),
                SlotSet('jenkins_job_buildnumber', None),
                SlotSet('requested_slot', 'jenkins_pipeline_name'),
            ]


class ActionJenkinsNotify(Action):
    def name(self) -> Text:
        return "action_jenkins_notify"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message.get('entities')
        build_number = next(
            (x['value'] for x in entities if x['entity'] == 'build_number'),
            None
        )
        job_name = next(
            (x['value'] for x in entities if x['entity'] == 'job_name'),
            None
        )
        running, build_status, timestamp, estimated_duration = get_jenkins_build_info(job_name, build_number)
        if running:
            logger.info(
                f'流水线:[{job_name}],正在构建，时间:[{timestamp}],预估时间:[{estimated_duration}]'
            )

            reminder = ReminderScheduled(
                "EXTERNAL_jenkins_reminder",
                trigger_date_time=datetime.datetime.now() + datetime.timedelta(seconds=5),
                entities={
                    "build_number": build_number,
                    "job_name": job_name
                },
                name='jenkins_reminder',
                kill_on_user_message=False,
            )
            return [reminder]
        else:
            logger.info(f'流水线构建完成:[{job_name}],状态为:[{build_status}]')
            if build_status == 'SUCCESS':
                dispatcher.utter_message(f"流水线{job_name}构建完成")
            else:
                dispatcher.utter_message(f"流水线{job_name}构建失败")
                dispatcher.utter_message(f"开始分析构建构建失败原因，请稍等......")
                results = analyze_jenkins_build_console(job_name, build_number)
                dispatcher.utter_message(f"分析建议:[{results}]")
            return []


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
