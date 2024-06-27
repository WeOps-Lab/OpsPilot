import os
from typing import Text, Dict, Any, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from utils.eventbus import EventBus
from utils.rasa_utils import RasaUtils


class ActionExternalUtter(Action):
    def __init__(self):
        self.bot_id = os.getenv('MUNCHKIN_BOT_ID', "")
        self.queue_name = f"enterprise_wechat_bot_channel_{self.bot_id}"

    def name(self) -> Text:
        return "action_external_utter"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        content = RasaUtils.get_tracker_entity(tracker, 'content')
        RasaUtils.log_info(tracker,
                           f'接收到主动触发回复请求,内容为: {content},通信渠道为: {tracker.get_latest_input_channel()}')

        if tracker.get_latest_input_channel() == "enterprise_wechat":
            RasaUtils.log_info(tracker, "发送企业微信机器人消息")
            sender_id = tracker.sender_id
            data = {
                "event_type": "notification_event",
                "notification_content": content,
                "sender_id": sender_id
            }
            eventbus = EventBus()
            eventbus.publish(self.queue_name, data)
        else:
            dispatcher.utter_message(content)
