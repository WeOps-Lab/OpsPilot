import datetime
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import ReminderScheduled
from rasa_sdk.executor import CollectingDispatcher

from actions.constant.server_settings import server_settings
from actions.utils.jenkins_utils import (analyze_jenkins_build_console,
                                         get_jenkins_build_info)


class ActionJenkinsNotify(Action):
    def name(self) -> Text:
        return "action_jenkins_notify"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if server_settings.enable_jenkins_skill is False:
            dispatcher.utter_message('OpsPilot没有启用Jenkins自动化能力....')
            return []

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
