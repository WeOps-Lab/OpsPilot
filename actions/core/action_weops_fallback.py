import os
from typing import Any, Text, Dict, List

from markdownify import markdownify as md
from rasa_sdk import Action, Tracker, logger
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

from actions.utils.azure_utils import query_chatgpt


class ActionWeOpsFallback(Action):

    def name(self) -> Text:
        return "action_weops_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_msg = tracker.latest_message['text']
        system_prompt = os.getenv('FALLBACK_PROMPT')
        run_mode = os.getenv('RUN_MODE')

        logger.info(f'无法识别用户的意图，进入默认Fallback，用户输入的信息为:{user_msg}')
        
        if tracker.active_loop_name is None:
            if run_mode == 'DEV':
                dispatcher.utter_message(text='WeOps Debug Fallback')
                return [UserUtteranceReverted()]
            else:
                dispatcher.utter_message(text='WeOps助理正在思考中........')
                result = query_chatgpt(system_prompt, user_msg)
                dispatcher.utter_message(text=md(result))
                return [UserUtteranceReverted()]
        else:
            return []
