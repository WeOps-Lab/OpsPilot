from langserve import CustomUserType


class PyodAnomalyPoint(CustomUserType):
    timestamp: int
    score: float
