import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import statsmodels.tsa.api as smt
from statsmodels.tsa.seasonal import seasonal_decompose
from pyramid.arima import auto_arima
from arch import arch_model


class Model:

    def __init__(self, data):
        self.__data = data
        self.model = {}
        self.res = []

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

        self.model.fit(self.__data)

    def predict(self, horizon):
        future_forecast = self.model.predict(n_periods=horizon)

        # This returns an array of predictions:

        print(future_forecast)

        future_forecast = pd.DataFrame(future_forecast, index=self.test.index, columns=['Prediction'])

        pd.concat([self.__data, future_forecast], axis=1).plot()

        plt.show()

        return future_forecast
