import os.path
from typing import Any, Text, Dict, List

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
        self.searcher = Searcher()

        embeddings = HuggingFaceEmbeddings(model_name='shibing624/text2vec-base-chinese',
                                           cache_folder='cache/models',
                                           encode_kwargs={
                                               'show_progress_bar': True,
                                               'normalize_embeddings': True
                                           })
        if server_settings.vec_db_path is not None and os.path.exists(
                server_settings.vec_db_path) and server_settings.fallback_chat_mode == 'knowledgebase':
            self.doc_search = FAISS.load_local(server_settings.vec_db_path, embeddings)
        else:
            self.doc_search = None

    def name(self) -> Text:
        return "action_weops_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message['text']

        run_mode = server_settings.run_mode

        logger.info(f'无法识别用户的意图，进入默认Fallback，用户输入的信息为:{user_msg}')

        if 'intent_ranking' in tracker.latest_message:
            logger.info(f'TOP3 Intent结果如下：{tracker.latest_message["intent_ranking"][0:3]}')

        if tracker.active_loop_name is None:
            if run_mode == 'DEV':
                dispatcher.utter_message(text='OpsPilot当前运行在开发模式，没有办法回复这些复杂的问题哦')
                return [UserUtteranceReverted()]
            else:
                try:

                    if server_settings.openai_endpoint is None:
                        dispatcher.utter_message(text='WeOps智能助理联网检索能力没有打开,无法回答这个问题.')
                        return [UserUtteranceReverted()]

                    if server_settings.fallback_chat_mode == 'knowledgebase':
                        if self.doc_search is None:
                            dispatcher.utter_message(f'我没有学习到任何信息，没法回复')
                            return [UserUtteranceReverted()]
                        else:
                            prompt_template = RedisUtils.get_prompt_template()
                            prompt_template = self.searcher.format_prompt(prompt_template, user_msg)

                            result = langchain_qa(self.doc_search, prompt_template, user_msg)

                            logger.info(f'GPT本地知识问答:问题[{user_msg}],回复:[{result}]')
                            dispatcher.utter_message(text=result['result'])
                    elif server_settings.fallback_chat_mode == 'online_knowledgebase':
                        result = chat_online(user_msg)
                        logger.info(f'GPT本地知识问答:问题[{user_msg}],回复:[{result}]')
                        dispatcher.utter_message(text=result)
                    else:
                        events = list(
                            filter(lambda x: x.get("event") == "user" or x.get("event") == "bot" and x.get(
                                "text") != server_settings.default_thinking_message,
                                   tracker.events))
                        user_messages = []
                        for event in reversed(events):
                            if len(user_messages) >= server_settings.chatgpt_model_max_history:
                                break
                            user_messages.insert(0, event.get("text"))

                        user_prompt = ''
                        for user_message in user_messages:
                            user_prompt += user_message + '\n'
                        user_prompt += user_msg

                        if user_prompt != '':
                            system_prompt = RedisUtils.get_fallback_prompt()
                            result = query_chatgpt(system_prompt, user_prompt)

                        logger.info(f'GPT问答模式:问题[{user_msg}],回复:[{result}]')
                        dispatcher.utter_message(text=result)
                except Exception as e:
                    logger.exception('请求Azure OpenAI 服务异常')
                    dispatcher.utter_message(text='OpsPilot处于非常繁忙的状态，请稍后再试.')
                return [UserUtteranceReverted()]
        else:
            return []
