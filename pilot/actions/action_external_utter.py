import json
import os
from typing import Text, Dict, Any, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from utils.eventbus import EventBus
from utils.rasa_utils import RasaUtils


class ActionExternalUtter(Action):

    def name(self) -> Text:
        return "action_external_utter"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        external_utter_content = RasaUtils.get_tracker_entity(tracker, 'external_utter_content')
        external_utter_channel = RasaUtils.get_tracker_entity(tracker, 'external_utter_channel')

        RasaUtils.log_info(tracker,
                           f'接收到主动触发回复请求,内容为: {external_utter_content},通信渠道为: {external_utter_channel}')

        if external_utter_channel in ["enterprise_wechat"]:
            RasaUtils.log_info(tracker, "发送通知到消息总线")

            sender_id = tracker.sender_id
            eventbus = EventBus()
            eventbus.publist_notification_event(external_utter_content, sender_id)
        else:
            dispatcher.utter_message(external_utter_content)
