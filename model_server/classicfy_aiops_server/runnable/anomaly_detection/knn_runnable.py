from typing import List

from langchain_core.runnables import RunnableLambda
from pyod.models.abod import ABOD

from runnable.anomaly_detection.pyod_base_runnable import PyodBaseRunnable
from user_types.anomaly_detection.knn_request import KnnRequest
from user_types.anomaly_detection.pyod_anomaly_point import PyodAnomalyPoint


class KnnRunnable(PyodBaseRunnable):
    def execute(self, request: KnnRequest) -> List[PyodAnomalyPoint]:
        clf = ABOD()
        return self.predict(request, clf)

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=KnnRequest, output_type=PyodAnomalyPoint)
