from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from utils.core_logger import log_info
from utils.redis_utils import RedisUtils


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
        key = f'{tracker.sender_id}_ticket_summary'
        ticket_summary = RedisUtils.get_value(key)
        RedisUtils.delete_value(key)
        log_info(tracker, f'解析工单信息,内容为: {ticket_summary}')

        return [SlotSet("in_ticket_submission", False)]
