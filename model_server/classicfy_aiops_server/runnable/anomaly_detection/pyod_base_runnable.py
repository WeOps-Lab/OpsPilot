import base64
from io import StringIO

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from user_types.anomaly_detection.pyod_anomaly_point import PyodAnomalyPoint
from user_types.anomaly_detection.pyod_base_request import PyodBaseRequest


class PyodBaseRunnable:
    def predict(self, request: PyodBaseRequest,clf):
        content = base64.b64decode(request.file.encode("utf-8")).decode("utf-8")
        data = pd.read_csv(StringIO(content))
        X = data['value']
        y = data['label']
        X_train = np.array(X)
        X_train = X_train.reshape(-1, 1)
        y_train = np.array(y)
        y_train = y_train.reshape(-1, 1)

        clf.fit(X_train, y_train)

        response = []
        for index, (pred, score) in enumerate(zip(clf.labels_, clf.decision_scores_)):
            if pred == 1:  # Check if the point is an anomaly
                timestamp = data.iloc[index]['timestamp']
                anomaly_point = PyodAnomalyPoint(timestamp=timestamp, score=float(score))
                response.append(anomaly_point)
        return response
