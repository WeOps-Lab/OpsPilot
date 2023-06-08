from typing import Any, Text, Dict, List

from markdownify import markdownify as md
from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.constant.server_settings import server_settings
from actions.utils.azure_utils import query_chatgpt


class ActionWeOpsPreFallback(Action):

    def name(self) -> Text:
        return "action_pre_weops_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text='WeOps助理正在思考中........')

        return []


class ActionWeOpsPostFallback(Action):

    def name(self) -> Text:
        return "action_post_weops_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return []


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

        if tracker.active_loop_name is None:
            if run_mode == 'DEV':
                dispatcher.utter_message(text='WeOps Debug Fallback')
                return [UserUtteranceReverted()]
            else:
                try:
                    result = query_chatgpt(system_prompt, user_msg)
                    dispatcher.utter_message(text=result)
                except Exception as e:
                    logger.exception('请求Azure OpenAI 服务异常')
                    dispatcher.utter_message(text='WeOps智能助理处于非常繁忙的状态，请稍后再试.')
                return [UserUtteranceReverted()]
        else:
            return []
