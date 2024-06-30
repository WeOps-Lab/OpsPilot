from typing import Optional, List

from langserve import CustomUserType

from user_types.chat_history import ChatHistory


class OpenAIChatRequest(CustomUserType):
    system_message_prompt: Optional[str] = ''
    openai_api_base: str = 'https://api.openai.com'
    openai_api_key: str
    temperature: float = 0.7
    model: str = 'gpt-3.5-turbo-16k'
    user_message: str
    chat_history: List[ChatHistory] = []
    conversation_window_size: Optional[int] = 10
    rag_context: Optional[str] = ''
