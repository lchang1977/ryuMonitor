import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


class Sarima_best:

    def __init__(self, data):
        data = data.astype(float)
        self.__data = data
        self._firstTime = True
        self.model = {}
        self.results = []
        print(self.__data.head())
        plt.plot(self.__data)
        # self.__data.plot()
        plt.show()

    def fit(self):
        # apply the model with best parameters found so far
        if self._firstTime:
            self.model = sm.tsa.statespace.SARIMAX(self.__data,
                                                   order=(0, 1, 1),
                                                   seasonal_order=(0, 1, 0, 12),
                                                   enforce_stationarity=False,
                                                   enforce_invertibility=False)
            self._firstTime = False
        else:
            self.model = sm.tsa.statespace.SARIMAX(self.__data,
                                                   order=(1, 1, 1),
                                                   seasonal_order=(0, 1, 1, 12),
                                                   enforce_stationarity=False,
                                                   enforce_invertibility=False)

        self.results = self.model.fit()

    def show_and_save(self, forecast):
        pd.concat([self.__data, forecast], axis=1).plot()
        plt.savefig('graph-{}.pdf'.format(forecast.index[0]))
        plt.show()

    def predict(self, horizon, sample_frequency):
        pred = self.results.get_forecast(steps=horizon)

        # Get confidence intervals of forecasts
        pred_ci = pred.conf_int()

        future_ts = [v + pd.to_timedelta(sample_frequency * (i + 1), unit='s')
                     for i, v in enumerate([self.__data.index[-1]] * horizon)]
        future_forecast = pd.DataFrame(pred.predicted_mean.values, index=future_ts, columns=['Prediction'])

        self.show_and_save(future_forecast)

        return future_forecast
