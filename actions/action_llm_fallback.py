from typing import Text, Any, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from core.server_settings import server_settings
from utils.llm_driver import LLMDriver
from utils.rasa_utils import RasaUtils


class ActionLLMFallback(Action):
    def __init__(self) -> None:
        super().__init__()

        self.llm_driver = LLMDriver(prompt=server_settings.prompt['action_llm_fallback']['prompt'])

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

        user_msg = RasaUtils.load_chat_history(tracker, server_settings.chatgpt_model_max_history)

        try:
            RasaUtils.log_info(tracker, f"用户输入的信息为:{tracker.latest_message['text']}")

            if user_msg != '':
                response_msg = self.llm_driver.chat(user_msg)
                dispatcher.utter_message(text=response_msg)

                RasaUtils.log_info(tracker, f"返回的信息为:{response_msg}")
            return []

        except Exception as e:
            RasaUtils.log_error(tracker, f"请求服务异常:{e},用户输入的信息为:{user_msg}")
            dispatcher.utter_message(text="OpsPilot服务异常，请稍后重试")
            return [UserUtteranceReverted()]
