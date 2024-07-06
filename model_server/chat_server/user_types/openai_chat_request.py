from user_types.base_chat_request import BaseChatRequest


class OpenAIChatRequest(BaseChatRequest):
    openai_api_base: str = 'https://api.openai.com'
    openai_api_key: str
    model: str = 'gpt-3.5-turbo-16k'
