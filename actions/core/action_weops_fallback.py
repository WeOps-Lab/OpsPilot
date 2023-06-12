from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.constant.server_settings import server_settings
from actions.utils.azure_utils import query_chatgpt


class ActionWeOpsFallback(Action):

    def name(self) -> Text:
        return "action_weops_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message['text']
        system_prompt = server_settings.fallback_prompt
        run_mode = server_settings.run_mode

        logger.info(f'无法识别用户的意图，进入默认Fallback，用户输入的信息为:{user_msg}')
        logger.info(f'TOP3 Intent结果如下：{tracker.latest_message["intent_ranking"][0:3]}')
        if tracker.active_loop_name is None:
            if run_mode == 'DEV':
                dispatcher.utter_message(text='OpsPilot当前运行在开发模式，没有办法回复这些复杂的问题哦')
                return [UserUtteranceReverted()]
            else:
                try:
                    events = list(filter(lambda x: x.get("event") == "user" and x.get("text"), tracker.events))
                    user_messages = []
                    for event in reversed(events):
                        if len(user_messages) >= 10:
                            break
                        user_messages.insert(0, event.get("text"))
                    user_prompt = ''
                    for user_message in user_messages:
                        user_prompt += user_message + '\n'
                    user_prompt += user_msg

                    if user_prompt != '':
                        result = query_chatgpt(system_prompt, user_prompt)
                        dispatcher.utter_message(text=result)
                except Exception as e:
                    logger.exception('请求Azure OpenAI 服务异常')
                    dispatcher.utter_message(text='WeOps智能助理处于非常繁忙的状态，请稍后再试.')
                return [UserUtteranceReverted()]
        else:
            return []
