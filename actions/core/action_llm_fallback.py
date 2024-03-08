import json
import os
from typing import Text, Any, Dict, List

import requests
from rasa_sdk import Action, Tracker, logger
from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.constants.server_settings import server_settings
from actions.utils.langchain_utils import LangChainUtils


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
            logger.warning(f"当前处于[{tracker.active_loop_name}]循环中,不执行Fallback操作")
            return []
        run_mode = server_settings.run_mode
        user_msg = tracker.latest_message["text"]

        logger.info(f"无法识别用户的意图，进入默认Fallback，用户输入的信息为:{user_msg}，当前运行模式为:[{run_mode}]")

        if run_mode == "dev":
            dispatcher.utter_message(text="RasaPilot当前运行在开发模式,不对内容进行回复")
            return [UserUtteranceReverted()]

        if server_settings.llm_fallback_mode == "OPEN_AI":
            try:
                response_msg = LangChainUtils.chat_llm_with_memory(tracker.sender_id, tracker.latest_message["text"])
                dispatcher.utter_message(text=response_msg)
                return []
            except Exception as e:
                logger.exception(f"请求OPEN_AI服务异常:{e}")
                dispatcher.utter_message(text="OpsPilot服务异常，请稍后重试")
                return [UserUtteranceReverted()]

        if server_settings.llm_fallback_mode == "DIFY":
            try:
                headers = {
                    "Authorization": f"Bearer {server_settings.dify_key}",
                    "Content-Type": "application/json",
                }
                data = {
                    "inputs": {},
                    "query": tracker.latest_message["text"],
                    "response_mode": "streaming",
                    "conversation_id": "",
                    "user": tracker.sender_id
                }
                response = requests.post(server_settings.dify_endpoint, headers=headers, json=data, stream=True)
                response.raise_for_status()
                response_msg = ""
                for line in response.iter_lines():
                    if line:
                        json_data = json.loads(line.decode('utf-8')[5:])
                        if 'answer' in json_data:
                            response_msg += json_data['answer']
                dispatcher.utter_message(text=response_msg)
                return []
            except Exception as e:
                logger.exception(f"请求DIFY服务异常:{e}")
                dispatcher.utter_message(text="OpsPilot服务异常，请稍后重试")
                return [UserUtteranceReverted()]

        if server_settings.llm_fallback_mode == "FAST_GPT":
            try:
                headers = {
                    "Authorization": f"Bearer {server_settings.fastgpt_key}",
                    "Content-Type": "application/json",
                }
                data = {
                    "chatId": tracker.sender_id,
                    "stream": False,
                    "detail": False,
                    "messages": [
                        {"content": tracker.latest_message["text"], "role": "user"}
                    ],
                }
                response = requests.post(
                    server_settings.fastgpt_endpoint,
                    headers=headers,
                    data=json.dumps(data),
                )
                response_msg = response.json()["choices"][0]["message"]["content"]
                dispatcher.utter_message(text=response_msg)
                return []
            except Exception as e:
                logger.exception(f"请求FAST_GPT服务异常:{e}")
                dispatcher.utter_message(text="OpsPilot服务异常，请稍后重试")
                return [UserUtteranceReverted()]
