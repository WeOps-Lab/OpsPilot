import json
from typing import Text, Any, Dict, List

import requests
from rasa_sdk import Action, Tracker
from rasa_sdk import logger
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.constants.server_settings import server_settings
from actions.services.dify_service import DifyService
from actions.services.fastgpt_service import FastGptService


class ActionLLMFallback(Action):
    def __init__(self) -> None:
        super().__init__()

        self.dify_service = DifyService(server_settings.dify_endpoint, server_settings.dify_key)
        self.fastgpt_service = FastGptService(server_settings.fastgpt_endpoint, server_settings.fastgpt_key)

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

        logger.info(f"无法识别用户的意图，进入默认Fallback，用户输入的信息为:{user_msg}，当前运行模式为:[{run_mode}]")

        if run_mode == "dev":
            dispatcher.utter_message(text="RasaPilot当前运行在开发模式,不对内容进行回复")
            return [UserUtteranceReverted()]

        try:
            if server_settings.fallback_llm == "FAST_GPT":
                response_msg = self.fastgpt_service.chat(tracker.sender_id, user_msg)
                dispatcher.utter_message(text=response_msg)
                logger.info(f"用户输入的信息为:{user_msg}，FastGPT返回的信息为:{response_msg}")
                return []
            else:
                events = list(
                    filter(
                        lambda x: x.get("event") == "user"
                                  or x.get("event") == "bot"
                                  and x.get("text") != server_settings.default_thinking_message,
                        tracker.events,
                    )
                )
                user_messages = []
                for event in reversed(events):
                    if len(user_messages) >= server_settings.chatgpt_model_max_history:
                        break
                    user_messages.insert(0, event)
                user_prompt = ""
                for user_message in user_messages:
                    user_prompt += f"{user_message['event']}:{user_message['text']}\n"

                response_msg = self.dify_service.chat(server_settings.dify_endpoint, server_settings.dify_key,
                                                      tracker.sender_id,
                                                      user_prompt)
                dispatcher.utter_message(text=response_msg)
                logger.info(f"用户输入的信息为:{user_msg}，DIFY返回的信息为:{response_msg}")
                return []

        except Exception as e:
            logger.exception(f"请求服务异常:{e}")
            dispatcher.utter_message(text="OpsPilot服务异常，请稍后重试")
            return [UserUtteranceReverted()]
