from actions.constants.server_settings import server_settings
from actions.services.fastgpt_service import FastGptService


def test_chat():
    service = FastGptService(server_settings.fastgpt_endpoint, server_settings.fastgpt_key)
    result = service.chat("sender_id", "介绍一下你自己")
    print(result)
