from typing import Text, Any, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk import logger
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.constants.server_settings import server_settings
from actions.services.chat_service import ChatService


class ActionLLMFallback(Action):
    def __init__(self) -> None:
        super().__init__()
        self.chat_service = ChatService(server_settings.fastgpt_endpoint, server_settings.fastgpt_key)

    def name(self) -> Text:
        return "action_llm_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if tracker.active_loop_name is not None:
            logger.warning(f"当前处于[{tracker.active_loop_name}]循环中,不执行Fallback操作")
            return []

        run_mode = server_settings.run_mode
        user_msg = tracker.latest_message["text"]

        logger.info(f"[大模型问答]用户输入的信息为:{user_msg}，当前运行模式为:[{run_mode}]")

        if run_mode == "dev":
            dispatcher.utter_message(text="RasaPilot当前运行在开发模式,不对内容进行回复")
            return [UserUtteranceReverted()]

        try:
            response_msg = self.chat_service.chat(tracker.sender_id, user_msg)
            dispatcher.utter_message(text=response_msg)
            logger.info(f"用户输入的信息为:{user_msg}，返回的信息为:{response_msg}")
            return []

        except Exception as e:
            logger.exception(f"请求服务异常:{e}")
            dispatcher.utter_message(text="OpsPilot服务异常，请稍后重试")
            return [UserUtteranceReverted()]
