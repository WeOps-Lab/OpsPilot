from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.services.kscan_service import KScanService


class ActionScanJob(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_scan_job"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        service = KScanService()

        scan_targets = tracker.get_slot("scan_targets")

        logger.info(f'开始扫描:[{scan_targets}]')
        scan_result = service.scan(scan_targets)
        dispatcher.utter_message('扫描结果如下：')
        dispatcher.utter_message(scan_result)
        return [SlotSet('scan_targets', None)]
