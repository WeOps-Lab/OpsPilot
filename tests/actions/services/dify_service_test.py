from dotenv import load_dotenv

from actions.constants.server_settings import server_settings
from actions.services.dify_service import DifyService


def test_chat():
    load_dotenv()
    service = DifyService()
    response = service.chat(server_settings.dify_endpoint, server_settings.dify_key, "sender_id", "介绍一下你自己")
    print(response)
