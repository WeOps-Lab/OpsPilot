from typing import List

from langchain_core.runnables import RunnableLambda
from pyod.models.ecod import ECOD

from runnable.anomaly_detection.pyod_base_runnable import PyodBaseRunnable
from user_types.anomaly_detection.ecod_request import EcodRequest
from user_types.anomaly_detection.pyod_anomaly_point import PyodAnomalyPoint


class EcodRunnable(PyodBaseRunnable):
    def execute(self, request: EcodRequest) -> List[PyodAnomalyPoint]:
        clf = ECOD()
        return self.predict(request, clf)

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=EcodRequest, output_type=PyodAnomalyPoint)
