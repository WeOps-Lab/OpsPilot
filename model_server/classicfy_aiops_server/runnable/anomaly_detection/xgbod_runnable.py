from typing import List

from langchain_core.runnables import RunnableLambda
from pyod.models.abod import ABOD
from pyod.models.xgbod import XGBOD

from runnable.anomaly_detection.pyod_base_runnable import PyodBaseRunnable
from user_types.anomaly_detection.abod_request import AbodRequest
from user_types.anomaly_detection.pyod_anomaly_point import PyodAnomalyPoint
from user_types.anomaly_detection.xgbod_request import XgbodRequest


class XgbodRunnable(PyodBaseRunnable):
    def execute(self, request: XgbodRequest) -> List[PyodAnomalyPoint]:
        clf = XGBOD()
        return self.predict(request, clf)

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=XgbodRequest, output_type=PyodAnomalyPoint)
