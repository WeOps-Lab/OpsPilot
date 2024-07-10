from typing import List

from langchain_core.runnables import RunnableLambda
from pyod.models.inne import INNE

from runnable.anomaly_detection.pyod_base_runnable import PyodBaseRunnable
from user_types.anomaly_detection.inne_request import InneRequest
from user_types.anomaly_detection.pyod_anomaly_point import PyodAnomalyPoint


class InneRunnable(PyodBaseRunnable):
    def execute(self, request: InneRequest) -> List[PyodAnomalyPoint]:
        clf = INNE(max_samples=4)
        return self.predict(request, clf)

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=InneRequest, output_type=PyodAnomalyPoint)
