from langserve import CustomUserType


class OnlineSearchRequest(CustomUserType):
    query: str
