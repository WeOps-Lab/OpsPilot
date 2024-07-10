from typing import List

from langchain_core.runnables import RunnableLambda
from pyod.models.iforest import IForest

from runnable.anomaly_detection.pyod_base_runnable import PyodBaseRunnable
from user_types.anomaly_detection.iforest_request import IForestRequest
from user_types.anomaly_detection.pyod_anomaly_point import PyodAnomalyPoint


class IForestRunnable(PyodBaseRunnable):
    def execute(self, request: IForestRequest) -> List[PyodAnomalyPoint]:
        clf = IForest()
        return self.predict(request, clf)

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=IForestRequest, output_type=PyodAnomalyPoint)
