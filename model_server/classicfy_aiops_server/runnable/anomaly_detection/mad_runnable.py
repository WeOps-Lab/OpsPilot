from typing import List

from langchain_core.runnables import RunnableLambda
from pyod.models.mad import MAD

from runnable.anomaly_detection.pyod_base_runnable import PyodBaseRunnable
from user_types.anomaly_detection.mad_request import MadRequest
from user_types.anomaly_detection.pyod_anomaly_point import PyodAnomalyPoint


class MadRunnable(PyodBaseRunnable):
    def execute(self, request: MadRequest) -> List[PyodAnomalyPoint]:
        clf = MAD(threshold=request.threshold)
        return self.predict(request, clf)

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=MadRequest, output_type=PyodAnomalyPoint)
