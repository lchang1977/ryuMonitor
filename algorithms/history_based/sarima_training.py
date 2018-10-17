import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from pyramid.arima import auto_arima


class SarimaTrain:

    def __init__(self, data):
        self.__data = data
        self.model = {}
        self.train = []
        self.test = []

        # print(data.head())

        # Interpret index as timestamp
        self.__data.index = pd.to_datetime(self.__data.index)

        # Rename column
        self.__data.columns = ['Energy Production']

        '''plt.plot(self.__data)
        plt.show()

        result = seasonal_decompose(self.__data, model='multiplicative')
        fig = result.plot()
        fig.show()'''

    def fit(self, train_size='2016-12-01'):
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

        self.train = self.__data[:train_size]
        if type(train_size) is str:
            index = len(self.__data)
            index = list(self.__data.index).index(pd.to_datetime(train_size))
            if index >= 30:
                index -= 30
        elif train_size >= 30:
            index = train_size - 30
        else:
            index = train_size
        self.test = self.__data[index:]

        self.model.fit(self.train)

    def predict(self):
        future_forecast = self.model.predict(n_periods=len(self.test))

        # This returns an array of predictions:

        print(future_forecast)

        future_forecast = pd.DataFrame(future_forecast, index=self.test.index, columns=['Prediction'])

        pd.concat([self.test, future_forecast], axis=1).plot()
        pd.concat([self.__data, future_forecast], axis=1).plot()

        plt.show()

        return future_forecast


