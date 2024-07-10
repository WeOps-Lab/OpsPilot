from typing import List

from langchain_core.runnables import RunnableLambda
from pyod.models.kpca import KPCA

from runnable.anomaly_detection.pyod_base_runnable import PyodBaseRunnable
from user_types.anomaly_detection.kpca_request import KpcaRequest
from user_types.anomaly_detection.pyod_anomaly_point import PyodAnomalyPoint


class KpcaRunnable(PyodBaseRunnable):
    def execute(self, request: KpcaRequest) -> List[PyodAnomalyPoint]:
        clf = KPCA()
        return self.predict(request, clf)

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=KpcaRequest, output_type=PyodAnomalyPoint)
