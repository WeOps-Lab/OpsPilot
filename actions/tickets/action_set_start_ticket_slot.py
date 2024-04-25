from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from utils.core_logger import log_info
from utils.redis_utils import RedisUtils


class ActionSetStartTicketSlot(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_set_start_ticket_slot"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return [
            SlotSet("in_ticket_submission", True),
            SlotSet("revise_ticket", None),
        ]
