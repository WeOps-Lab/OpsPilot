from typing import List

from langchain_core.runnables import RunnableLambda
from pyod.models.abod import ABOD

from runnable.anomaly_detection.pyod_base_runnable import PyodBaseRunnable
from user_types.anomaly_detection.abod_request import AbodRequest
from user_types.anomaly_detection.pyod_anomaly_point import PyodAnomalyPoint


class AbodRunnable(PyodBaseRunnable):
    def execute(self, request: AbodRequest) -> List[PyodAnomalyPoint]:
        clf = ABOD()
        return self.predict(request, clf)

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=AbodRequest, output_type=PyodAnomalyPoint)
