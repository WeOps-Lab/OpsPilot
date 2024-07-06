from langchain_community.chat_models import ChatZhipuAI

from utils.base_driver import BaseDriver


class ZhipuDriver(BaseDriver):
    def __init__(self, api_base, api_key, temperature, model):
        self.client = ChatZhipuAI(
            api_base=api_base,
            api_key=api_key,
            model=model,
            temperature=temperature,
        )
