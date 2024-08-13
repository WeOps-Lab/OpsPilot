# SARIMA 
## Algorithm introduction 
 
SARIMA (Seasonal Autoregressive Integrated Moving Average) is a statistical model for time series forecasting that extends the ARIMA (autoregressive Integrated Moving Average) model. It is difficult for general time series data to meet the stationarity requirements, and the most commonly used conversion method is difference, so <font color=red>ARIMA(p,q,d)</font> includes the process of difference on the basis of <font color=red>ARMA(p,q)</font>. Therefore, ARIMA can handle non-stationary time series, but it can't handle periodic series well. Therefore, <font color=red>SARIMA(p,q,d,P,Q,D,s)</font> expands on the basis of <font color=red>ARIMA(p,q,d)</font> and adds three hyperparameters of P Q D and a seasonal cycle parameter s. Time series data with seasonal components can be supported. 
## Use scenario 
SARIMA is suitable for time series data with <font color=red> seasonal variation </font>, and the <font color=red> data volume is larger </font>, and the effect of the model with too little data is poor. 
 
## Algorithm principle 
SARIMA consists of four parts: seasonal correlation (S), autoregression (AR), difference (I), and average shift (MA) : 
 
(1) **AR (autoregressive) part ** indicates the dependency between the current value and the past value, that is, there is a linear relationship between the current value and the value of several past time points, and the appropriate lag order can be determined through PACF, corresponding to the parameter p; 
 
(2) **I (difference) part ** is to eliminate the non-stationarity of the data. Through differential processing of the time series data, the non-stationary time series data can be transformed into stable time series data, corresponding to parameter d; 
 
(3) **MA (moving average) part ** represents the dependence between the current value and the observed errors at several past time points, and the appropriate lag order can be determined by ACF, corresponding to parameter q; 
 
(4) **S (seasonal term) ** includes four parts: seasonal regression (SAR), seasonal difference (SI), seasonal moving average (SMA) and seasonal frequency (s), corresponding to parameters P, D, Q and s respectively. The first three seasonal terms have similar effects to their counterparts in the ARIMA model. 
 
In summary, the SARIMA model uses techniques such as autoregression, difference, and moving average, and takes into account seasonal correlation terms, to predict time series data with seasonality and trend.