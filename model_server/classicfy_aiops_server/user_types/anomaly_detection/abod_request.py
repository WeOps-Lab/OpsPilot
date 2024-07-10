from langserve import CustomUserType
from pydantic.v1 import Field

from user_types.anomaly_detection.pyod_base_request import PyodBaseRequest


class AbodRequest(PyodBaseRequest):
    pass
