import datetime
import logging
from typing import Text, Dict, Any, List

from loguru import logger
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, ReminderScheduled
from rasa_sdk.executor import CollectingDispatcher
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
        logger.info(f'启动扫描资产任务,当前对话通道:{tracker.get_latest_input_channel()}')
        scan_targets = tracker.get_slot("scan_targets")
        dispatcher.utter_message(f"开始对[{scan_targets}]进行资产测绘~,扫描结束后，小助手会第一时间通知你哟")
        scan_target.delay(tracker.sender_id, scan_targets)
        return [SlotSet('scan_targets', None)]
