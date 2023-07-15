from typing import Text, List, Any, Dict

from loguru import logger
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from actions.utils.core_utils import is_valid_url


class ValidateOnlineChatForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_online_chat_form"

    def validate_online_chat_url(
            self,
            slot_value: Any,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict,
    ) -> Dict[Text, Any]:
        if tracker.get_latest_input_channel() == 'slack':
            slot_value = slot_value[1:-1]
        if is_valid_url(slot_value):
            return {'online_chat_url': slot_value}
        else:
            logger.info(
                f'输入的URL地址不合法,当前输入的地址为:[{slot_value}],当前通道为[{tracker.get_latest_input_channel()}]')
            dispatcher.utter_message(f'输入的URL地址不合法,当前输入的地址为:[{slot_value}],请重新输入')
            return {'online_chat_url': None}
