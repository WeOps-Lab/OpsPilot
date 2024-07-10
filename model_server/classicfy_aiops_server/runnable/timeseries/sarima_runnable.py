import base64
from io import StringIO
from typing import List

import pandas as pd
import pmdarima as pm
from langchain_core.runnables import RunnableLambda
from statsmodels.tsa.statespace.sarimax import SARIMAX

from user_types.timeseries.sarima_request import SarimaRequest
from user_types.timeseries.timeseries_predict_point import TimeSeriesPredictPoint


class SarimaRunnable:
    def execute(self, request: SarimaRequest) -> List[TimeSeriesPredictPoint]:
        content = base64.b64decode(request.file.encode("utf-8")).decode("utf-8")
        data = pd.read_csv(StringIO(content), index_col='ds', parse_dates=True)
        model = pm.auto_arima(data,
                              start_p=0,  # p最小值
                              start_q=0,  # q最小值
                              test='adf',  # ADF检验确认差分阶数d
                              max_p=5,  # p最大值
                              max_q=5,  # q最大值
                              m=12,  # 季节性周期长度，当m=1时则不考虑季节性
                              d=None,  # 通过函数来计算d
                              seasonal=True, start_P=0, D=1, trace=True,
                              error_action='ignore', suppress_warnings=True,
                              stepwise=False  # stepwise为False则不进行完全组合遍历
                              )

        order = model.get_params()['order']
        seasonal_order = model.get_params()['seasonal_order']

        sarima_model = SARIMAX(data, order=order, seasonal_order=seasonal_order)
        sarima_result = sarima_model.fit()
        forecast = sarima_result.get_forecast(steps=request.predict_point)

        forecasted_points = []

        for date, value in forecast.predicted_mean.items():
            forecasted_point = TimeSeriesPredictPoint(timestamp=date.timestamp(), predict_value=value)
            forecasted_points.append(forecasted_point)

        return forecasted_points

    def instance(self):
        return RunnableLambda(self.execute).with_types(input_type=SarimaRequest,
                                                       output_type=List[TimeSeriesPredictPoint])
