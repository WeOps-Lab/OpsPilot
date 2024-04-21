from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.executor import CollectingDispatcher

from actions.services.kscan_service import KScanService


class ActionScanReminder(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_scan_reminder"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        service = KScanService()

        entities = tracker.latest_message.get('entities')
        scan_targets = next(
            (x['value'] for x in entities if x['entity'] == 'scan_targets'),
            None
        )
        logger.info(f'开始扫描:[{scan_targets}]')
        scan_result = service.scan(scan_targets)
        markdown_result = service.json_to_markdown(scan_result)
        dispatcher.utter_message('扫描结果如下：')
        dispatcher.utter_message(markdown_result)
