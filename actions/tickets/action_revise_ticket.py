import json
from typing import Text, Dict, Any, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.constants.server_settings import server_settings
from actions.services.chat_service import ChatService
from utils.rasa_utils import load_chat_history


class ActionReviseTicket(Action):
    def __init__(self):
        self.chat_service = ChatService(server_settings.fastgpt_endpoint, server_settings.fastgpt_ticket_key)

    def name(self) -> Text:
        return "action_revise_ticket"

    async def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        chat_history = load_chat_history(tracker, server_settings.chatgpt_model_max_history)
        ticket_summary = tracker.get_slot('ticket_summary')
        revise_ticket = tracker.get_slot('revise_ticket')
        prompt = f'''
            对话的历史信息:{chat_history}，总结的工单信息:{ticket_summary}
            用户对总结的工单信息提出了修改意见:{revise_ticket}
        '''
        ticket_summary = self.chat_service.chat(tracker.sender_id, prompt)

        dispatcher.utter_message('以下为您修改后的工单：')
        ticket_dict = json.loads(ticket_summary)
        ticket_dict_summary = ''
        for key, value in ticket_dict.items():
            ticket_dict_summary += f'{key}: {value}\n'
        dispatcher.utter_message(ticket_dict_summary)

        return [
            SlotSet("ticket_summary", ticket_summary),
        ]
