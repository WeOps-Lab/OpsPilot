import json
from typing import Text, Any, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from utils.munchkin_driver import MunchkinDriver


class ActionListJenkinsJobs(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_list_jenkins_jobs"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        munchkin = MunchkinDriver()

        result = munchkin.automation_skills_execute("list_jenkins_jobs", "", tracker.sender_id)

        keys = result['return'][0].keys()
        first_key = list(keys)[0]

        color_map = {
            'blue': '构建成功',
            'yellow': '构建不稳定',
            'red': '构建失败',
            'notbuilt': '尚未构建',
            'disabled': '被禁用',
            'aborted': '构建被中止',
            'blue_anime': '正在构建，上次成功',
            'yellow_anime': '正在构建，上次不稳定',
            'red_anime': '正在构建，上次失败'
        }
        jobs = json.loads(result['return'][0][first_key])['jobs']
        table_str = "| 名称 | 状态 |\n| --- | --- |\n"
        for job in jobs:
            if 'color' not in job:
                status = '未知'
            else:
                status = color_map.get(job['color'], '未知')
            table_str += f"| {job['name']} | {status} |\n"
        dispatcher.utter_message(table_str)
