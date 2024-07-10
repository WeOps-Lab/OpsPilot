from langserve import CustomUserType
from pydantic.v1 import Field

from user_types.anomaly_detection.pyod_base_request import PyodBaseRequest


class MadRequest(PyodBaseRequest):
    threshold: float = Field(3.5, extra={"widget": {"type": "number"}})
