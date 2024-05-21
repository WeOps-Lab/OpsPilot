from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from utils.rasa_utils import RasaUtils


class ActionExternalUtter(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_external_utter"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        content = RasaUtils.get_tracker_entity(tracker, 'content')
        RasaUtils.log_info(tracker, f'接收到主动触发回复请求,内容为: {content}')

        dispatcher.utter_message(content)
