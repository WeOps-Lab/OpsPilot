import logging

from actions.constants.server_settings import server_settings
from actions.services.chat_service import ChatService


def test_chat():
    service = ChatService(server_settings.fastgpt_endpoint, server_settings.fastgpt_key)
    result = service.chat("sender_id", "介绍一下你自己")
    logging.info(result)
