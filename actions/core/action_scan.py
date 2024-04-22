from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from utils.core_logger import log_info
from tasks.celery import scan_target


class ActionScan(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_scan"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        log_info(tracker, f'启动扫描资产任务....')

        scan_targets = tracker.get_slot("scan_targets")
        dispatcher.utter_message(f"开始对[{scan_targets}]进行资产测绘~,扫描结束后，小助手会第一时间通知你哟")

        scan_target.delay(tracker.get_latest_input_channel(), tracker.sender_id, scan_targets)
        return [SlotSet('scan_targets', None)]
