from typing import Text, Any, Dict, List

from langchain.memory import ChatMessageHistory
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from core.server_settings import server_settings
from utils.llm_driver import LLMDriver
from utils.rasa_utils import RasaUtils


class ActionLLMFallback(Action):
    def __init__(self) -> None:
        super().__init__()

        self.llm_driver = LLMDriver()

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
        chat_history = ChatMessageHistory()
        for event in converation_history:
            if event['event'] == 'user':
                chat_history.add_user_message(event['text'])
            elif event['event'] == 'bot':
                chat_history.add_ai_message(event['text'])

        try:
            if tracker.latest_message['text'] != '':
                response_msg = self.llm_driver.chat_with_history(
                    server_settings.prompt['action_llm_fallback']['history_prompt'],
                    tracker.latest_message['text'],
                    chat_history,
                    server_settings.chatgpt_model_max_history)
                dispatcher.utter_message(text=response_msg)
                RasaUtils.log_info(tracker, f"返回的信息为:{response_msg}")
            return []

        except Exception as e:

            RasaUtils.log_error(tracker, f"请求服务异常:{e},用户输入的信息为:{tracker.latest_message['text']}")
            dispatcher.utter_message(text="OpsPilot服务异常，请稍后重试")
            return [UserUtteranceReverted()]
