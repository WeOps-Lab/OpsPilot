from langserve import CustomUserType


class ChatHistory(CustomUserType):
    event: str
    text: str
