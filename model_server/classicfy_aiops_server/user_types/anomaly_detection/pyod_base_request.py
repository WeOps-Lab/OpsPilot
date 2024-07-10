from langserve import CustomUserType
from pydantic.v1 import Field


class PyodBaseRequest(CustomUserType):
    file: str = Field(..., extra={"widget": {"type": "base64file"}})
