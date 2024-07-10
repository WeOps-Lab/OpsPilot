from langserve import CustomUserType
from pydantic.v1 import Field


class HoltWinterRequest(CustomUserType):
    file: str = Field(..., extra={"widget": {"type": "base64file"}})
    seasonal: str = "add"
    trend: str = "add"
    seasonal_periods: int = 12
    predict_point: int = 10
