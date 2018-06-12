import pandas as pd
from arima import Arima

data = pd.read_csv("electric_Production.csv", index_col=0)
arima = Arima(data)
arima.fit()
arima.predict()


# arima.fit_with_garch(300)
# arima.predict_with_garch()