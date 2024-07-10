from langserve import CustomUserType
from pydantic.v1 import Field


class SarimaRequest(CustomUserType):
    file: str = Field(..., extra={"widget": {"type": "base64file"}})
    predict_point: int = 10
