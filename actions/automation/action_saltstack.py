import json
import os.path
from typing import Text, Dict, Any, List

from loguru import logger
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.constants.server_settings import server_settings
from actions.services.chat_service import ChatService
from tasks.celery import start_salt_job
from utils.core_logger import log_info


class ActionSaltStack(Action):
    def __init__(self):
        self.chat_service = ChatService(server_settings.fastgpt_endpoint, server_settings.fastgpt_automation_key)

    def name(self) -> Text:
        return "action_saltstack"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        log_info(tracker, f'开始执行SaltStack任务....')
        intent = tracker.get_intent_of_latest_message(True)

        # 检查intent_knowledge/automation/{intent} 目录是否存在
        if os.path.exists(f'intent_knowledge/automation/{intent}.md'):
            content = '这是我提供给你参考的官方文档：'
            with open(f'intent_knowledge/automation/{intent}.md', 'r', encoding='utf-8') as f:
                content += f.read()
            content += f'你的任务是:{tracker.latest_message["text"]}'
            response = self.chat_service.chat(tracker.sender_id, content)
            logger.info(f'执行SaltStack任务: {response}')
            data = json.loads(response)

            func = data['func']
            tgt = data['tgt']
            args = data['args']

            dispatcher.utter_message(f"开始执行任务,认为执行完后会通知你哟~")

            start_salt_job.delay(tracker.get_latest_input_channel(), tracker.sender_id, tracker.latest_message['text'],
                                 func,
                                 tgt, args)
        else:
            dispatcher.utter_message(f"抱歉，我还不知道如何处理这个任务，我会尽快学习的！")
        return []
