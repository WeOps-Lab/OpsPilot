from typing import Optional, List

from langserve import CustomUserType

from user_types.chat_history import ChatHistory


class BaseChatRequest(CustomUserType):
    system_message_prompt: Optional[str] = ''
    temperature: float = 0.7
    user_message: str
    chat_history: List[ChatHistory] = []
    conversation_window_size: Optional[int] = 10
    rag_context: Optional[str] = ''
