from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from utils.core_logger import log_info


class ActionStartTicket(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_start_ticket"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        ticket_summary = tracker.get_slot('ticket_summary')
        log_info(tracker, f'解析工单信息,内容为: {ticket_summary}')

        return []
