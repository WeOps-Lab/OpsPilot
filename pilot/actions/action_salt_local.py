from typing import Text, Any, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from utils.munchkin_driver import MunchkinDriver
from utils.rasa_utils import RasaUtils


class ActionSaltLocal(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_salt_local"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        munchkin = MunchkinDriver()
        salt_params = RasaUtils.get_tracker_entity(tracker, 'salt_params')
        RasaUtils.log_info(tracker, f"执行salt任务，参数: {salt_params}")
        result = munchkin.salt_local_execute(salt_params, tracker.sender_id)
        dispatcher.utter_message(f"执行结果: {result}")
