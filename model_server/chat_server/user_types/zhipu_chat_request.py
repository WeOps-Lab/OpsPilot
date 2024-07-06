from langchain_community.chat_models.zhipuai import ZHIPUAI_API_BASE

from user_types.base_chat_request import BaseChatRequest


class ZhipuChatRequest(BaseChatRequest):
    api_base: str = ZHIPUAI_API_BASE
    api_key: str
    model: str = 'glm-4'
