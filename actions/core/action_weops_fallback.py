from typing import Any, Text, Dict, List

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
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
        if server_settings.vec_db_path is not None:
            embeddings = HuggingFaceEmbeddings(model_name='shibing624/text2vec-base-chinese',
                                               cache_folder='cache/models',
                                               encode_kwargs={
                                                   'show_progress_bar': True
                                               })
            self.doc_search = Chroma(persist_directory=server_settings.vec_db_path, embedding_function=embeddings)

    def name(self) -> Text:
        return "action_weops_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message['text']

        run_mode = server_settings.run_mode

        logger.info(f'无法识别用户的意图，进入默认Fallback，用户输入的信息为:{user_msg}')
        logger.info(f'TOP3 Intent结果如下：{tracker.latest_message["intent_ranking"][0:3]}')

        # TODO: 先从本地知识文件中检索可能的内容，直接回复，假如没有，转给GPT进行查找总结

        if tracker.active_loop_name is None:
            if run_mode == 'DEV':
                dispatcher.utter_message(text='OpsPilot当前运行在开发模式，没有办法回复这些复杂的问题哦')
                return [UserUtteranceReverted()]
            else:
                try:
                    if server_settings.openai_endpoint is None:
                        dispatcher.utter_message(text='WeOps智能助理联网检索能力没有打开,无法回答这个问题.')
                        return [UserUtteranceReverted()]

                    events = list(filter(lambda x: x.get("event") == "user" and x.get("text"), tracker.events))
                    user_messages = []
                    for event in reversed(events):
                        if len(user_messages) >= 10:
                            break
                        user_messages.insert(0, event.get("text"))

                    if server_settings.fallback_chat_mode == 'knowledgebase':
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
                    dispatcher.utter_message(text='WeOps智能助理处于非常繁忙的状态，请稍后再试.')
                return [UserUtteranceReverted()]
        else:
            return []
