from typing import List

from langchain_core.runnables import RunnableLambda
from pyod.models.abod import ABOD
from pyod.models.ocsvm import OCSVM

from runnable.anomaly_detection.pyod_base_runnable import PyodBaseRunnable
from user_types.anomaly_detection.abod_request import AbodRequest
from user_types.anomaly_detection.ocssvm_request import OcsSvmRequest
from user_types.anomaly_detection.pyod_anomaly_point import PyodAnomalyPoint


class OcsSvmRunnable(PyodBaseRunnable):
    def execute(self, request: OcsSvmRequest) -> List[PyodAnomalyPoint]:
        clf = OCSVM()
        return self.predict(request, clf)

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=OcsSvmRequest, output_type=PyodAnomalyPoint)
