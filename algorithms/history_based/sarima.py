import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pyramid.arima import auto_arima


class Sarima:

    def __init__(self, data, comparing):
        data = data.astype(float)
        self.__data = data
        self._firstTime = True
        self._comparing = comparing
        self.model = {}
        self.results = []
        print(self.__data.head())
        plt.plot(self.__data)
        # self.__data.plot()
        plt.show()

    def fit(self):
        self.model = auto_arima(self.__data, start_p=1, start_q=1,
                                max_p=3, max_q=3, m=12,
                                start_P=0, seasonal=True,
                                d=1, D=1, trace=True,
                                error_action='ignore',
                                suppress_warnings=True,
                                stepwise=True)

        print('Best found AIC: %f' % (self.model.aic()))
        print('Arima model (%d, %d, %d) x (%d, %d, %d, %d) ' % (self.model.order[0],
              self.model.order[1], self.model.order[2],
              self.model.seasonal_order[0], self.model.seasonal_order[1],
              self.model.seasonal_order[2], self.model.seasonal_order[3]))

        # self.train = self.__data.loc['1985-01-01':'2016-12-01']
        # self.test = self.__data.loc['2015-01-01':]

        if self._comparing:
            line_to_write = 'AIC : {}, model ({}, {}, {}) x ({}, {}, {}, {})'.format(
                self.model.aic(), self.model.order[0],
                self.model.order[1], self.model.order[2],
                self.model.seasonal_order[0], self.model.seasonal_order[1],
                self.model.seasonal_order[2], self.model.seasonal_order[3])
            self.save_aic(self.__data.index[0], self.__data.index[-1], line_to_write)

        self.results = self.model.fit(self.__data)

    def show_and_save(self, forecast):
        pd.concat([self.__data, forecast], axis=1).plot()
        plt.savefig('graph-{}.pdf'.format(forecast.index[0]))
        plt.show()

    def save_aic(self, start_ts, last_ts, line):
        with open("past-aic.txt", "a") as file:
            file.write('{}-{} :'.format(start_ts, last_ts))
            file.write(line + '\n')

    def predict(self, horizon, sample_frequency):
        future_forecast = self.model.predict(n_periods=horizon)

        future_ts = [v + pd.to_timedelta(sample_frequency * (i + 1), unit='s')
                     for i, v in enumerate([self.__data.index[-1]]*horizon)]
        # This returns an array of predictions:

        print(future_forecast)

        future_forecast = pd.DataFrame(future_forecast, index=future_ts, columns=['Prediction'])

        self.show_and_save(future_forecast)

        return future_forecast
