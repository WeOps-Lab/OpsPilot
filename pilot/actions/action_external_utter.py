from typing import Text, Dict, Any, List

import requests
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
        channel = RasaUtils.get_tracker_entity(tracker, 'channel')
        RasaUtils.log_info(tracker, f'接收到主动触发回复请求,内容为: {content},通信渠道为: {channel}')

        dispatcher.utter_message(content)
