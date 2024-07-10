from typing import List

from langchain_core.runnables import RunnableLambda
from pyod.models.abod import ABOD
from pyod.models.copod import COPOD
from pyod.models.iforest import IForest
from pyod.models.lof import LOF
from pyod.models.suod import SUOD

from runnable.anomaly_detection.pyod_base_runnable import PyodBaseRunnable
from user_types.anomaly_detection.abod_request import AbodRequest
from user_types.anomaly_detection.pyod_anomaly_point import PyodAnomalyPoint
from user_types.anomaly_detection.suod_request import SuodRequest


class SuodRunnable(PyodBaseRunnable):
    def execute(self, request: SuodRequest) -> List[PyodAnomalyPoint]:
        detector_list = [LOF(n_neighbors=15), LOF(n_neighbors=20),
                         LOF(n_neighbors=25), LOF(n_neighbors=35),
                         COPOD(), IForest(n_estimators=100),
                         IForest(n_estimators=200)]
        clf = SUOD(base_estimators=detector_list, n_jobs=2, combination='average', verbose=False)

        return self.predict(request, clf)

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=SuodRequest, output_type=PyodAnomalyPoint)
