import base64
from io import StringIO
from typing import List
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from langchain_core.runnables import RunnableLambda
import pandas as pd

from user_types.timeseries.holt_winter_request import HoltWinterRequest
from user_types.timeseries.timeseries_predict_point import TimeSeriesPredictPoint


class HoltWinterRunnable:
    def execute(self, request: HoltWinterRequest) -> List[TimeSeriesPredictPoint]:
        content = base64.b64decode(request.file.encode("utf-8")).decode("utf-8")
        data = pd.read_csv(StringIO(content), index_col='ds', parse_dates=True)

        model = ExponentialSmoothing(data['y'], trend=request.trend, seasonal=request.seasonal,
                                     seasonal_periods=request.seasonal_periods).fit()
        prediction_results = model.forecast(request.predict_point)

        forecasted_points = []

        for date, value in prediction_results.items():
            forecasted_point = TimeSeriesPredictPoint(timestamp=date.timestamp(), predict_value=value)
            forecasted_points.append(forecasted_point)

        return forecasted_points

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=HoltWinterRequest,
                                                       output_type=List[TimeSeriesPredictPoint])
