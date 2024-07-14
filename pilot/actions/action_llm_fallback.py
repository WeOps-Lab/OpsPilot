from typing import Text, Any, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from utils.munchkin_driver import MunchkinDriver
from utils.rasa_utils import RasaUtils


class ActionLLMFallback(Action):
    def __init__(self) -> None:
        super().__init__()

    def name(self) -> Text:
        return "action_llm_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if tracker.active_loop_name is not None:
            RasaUtils.log_info(tracker, f"当前处于[{tracker.active_loop_name}]循环中,不执行Fallback操作")
            return []

        converation_history = RasaUtils.load_chat_history(tracker)
        munchkin = MunchkinDriver()

        try:
            if tracker.latest_message['text'] != '':
                result = munchkin.chat('action_llm_fallback', tracker.latest_message['text'], converation_history,
                                       tracker.sender_id)
                dispatcher.utter_message(text=result)
                RasaUtils.log_info(tracker, f"返回的信息为:{result}")
            return []

        except Exception as e:
            RasaUtils.log_error(tracker, f"请求服务异常:{e},用户输入的信息为:{tracker.latest_message['text']}")
            dispatcher.utter_message(text="OpsPilot服务异常，请稍后重试")
            return [UserUtteranceReverted()]
