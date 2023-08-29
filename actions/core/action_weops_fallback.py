import json
import os.path
from typing import Any, Text, Dict, List

import requests
from langchain import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.constant.server_settings import server_settings
from actions.utils.indexer_utils import Searcher
from actions.utils.langchain_utils import langchain_qa, query_chatgpt, chat_online
from actions.utils.redis_utils import RedisUtils


class ActionWeOpsFallback(Action):
    def __init__(self) -> None:
        super().__init__()
        if server_settings.fallback_mode == "LOCAL_LLM":
            logger.info(f"Fallback模式为LOCAL_LLM")

            # 初始化本地搜索引擎
            self.searcher = Searcher()

            # 初始化向量模型
            embeddings = HuggingFaceEmbeddings(
                model_name=server_settings.embed_model_name,
                cache_folder=server_settings.embed_model_cache_home,
                encode_kwargs={"show_progress_bar": True, "normalize_embeddings": True},
            )

            # 判断本地向量数据库是否存在,并且fallback_chat_mode为knowledgebase，如果是则加载本地向量数据库
            if (
                    server_settings.vec_db_path is not None
                    and os.path.exists(server_settings.vec_db_path)
                    and server_settings.fallback_chat_mode == "knowledgebase"
            ):
                self.doc_search = FAISS.load_local(
                    server_settings.vec_db_path, embeddings
                )
            else:
                self.doc_search = None

        if server_settings.fallback_mode == "FAST_GPT":
            logger.info(f"Fallback模式为FAST_GPT,应用地址为:{server_settings.fastgpt_endpoint}")

    def name(self) -> Text:
        return "action_weops_fallback"

    def show_intent_ranking(self, tracker: Tracker):
        if "intent_ranking" in tracker.latest_message:
            # 判断intent的数量是否超过3，假如超过3个,则显示前3个Intent的结果,否则则显示所有intent的得分结果
            if len(tracker.latest_message["intent_ranking"]) > 3:
                logger.info(
                    f'TOP3 Intent结果如下：{tracker.latest_message["intent_ranking"][0:3]}'
                )
            else:
                logger.info(f'Intent结果如下：{tracker.latest_message["intent_ranking"]}')

    def answer_via_llm(
            self, user_msg, tracker: Tracker, dispatcher: CollectingDispatcher
    ):
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

        if user_prompt != "":
            system_prompt = RedisUtils.get_fallback_prompt()
            result = query_chatgpt(system_prompt, user_prompt)

        logger.info(f"GPT问答模式:问题[{user_msg}],回复:[{result}]")
        dispatcher.utter_message(text=result)
        return []

    def answer_via_knowledgebase(self, user_msg, dispatcher: CollectingDispatcher):
        if self.doc_search is None:
            dispatcher.utter_message(f"我没有学习到任何信息，无法回复")
            return [UserUtteranceReverted()]
        else:
            prompt_template = RedisUtils.get_prompt_template()
            prompt_template = self.searcher.format_prompt(prompt_template, user_msg)

            result = langchain_qa(self.doc_search, prompt_template, user_msg)

            logger.info(f"GPT本地知识问答:问题[{user_msg}],回复:[{result}]")
            dispatcher.utter_message(text=result["result"])
            return []

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        if tracker.active_loop_name is not None:
            logger.warning(f"当前处于[{tracker.active_loop_name}]循环中,不执行Fallback操作")
            return []

        user_msg = tracker.latest_message["text"]
        run_mode = server_settings.run_mode

        logger.info(f"无法识别用户的意图，进入默认Fallback，用户输入的信息为:{user_msg}，当前运行模式为:[{run_mode}]")
        self.show_intent_ranking(tracker)

        if run_mode == "DEV":
            dispatcher.utter_message(text="OpsPilot当前运行在开发模式，没有办法回复这些复杂的问题哦")
            return [UserUtteranceReverted()]

        if server_settings.fallback_mode == "LOCAL_LLM":
            if server_settings.openai_endpoint is None:
                dispatcher.utter_message(text="OpsPilot没有打开LLM回复的能力,无法回答这个问题.")
                return [UserUtteranceReverted()]

            try:
                if server_settings.fallback_chat_mode == "knowledgebase":
                    return self.answer_via_knowledgebase(user_msg, dispatcher)
                else:
                    return self.answer_via_llm(user_msg, tracker, dispatcher)

            except Exception as e:
                logger.exception("请求Azure OpenAI 服务异常")
                dispatcher.utter_message(text="OpsPilot处于非常繁忙的状态，请稍后再试.")
                return [UserUtteranceReverted()]

        if server_settings.fallback_mode == "FAST_GPT":
            if server_settings.fastgpt_endpoint is None:
                dispatcher.utter_message(text="OpsPilot没有打开FAST_GPT回复的能力,无法回答这个问题.")
                return [UserUtteranceReverted()]

            try:
                # 向FAST_GPT服务发起POST请求,数据格式为JSON
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
                logger.exception("请求FAST_GPT服务异常")
                dispatcher.utter_message(text="OpsPilot处于非常繁忙的状态，请稍后再试.")
                return [UserUtteranceReverted()]
