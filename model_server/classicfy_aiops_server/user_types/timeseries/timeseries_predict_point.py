from langserve import CustomUserType


class TimeSeriesPredictPoint(CustomUserType):
    timestamp: float
    predict_value: float
