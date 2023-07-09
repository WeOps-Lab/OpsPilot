from typing import Text, List, Any, Dict

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
        if is_valid_url(slot_value):
            return {'online_chat_url': slot_value}
        else:
            dispatcher.utter_message('输入的URL地址不合法,请重新输入')
            return {'online_chat_url': None}
