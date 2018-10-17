import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing


class HoltWinters:

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
        self.model = ExponentialSmoothing(self.__data['BW'],
                                          seasonal_periods=7,
                                          trend='add',
                                          seasonal='add', )

        self.results = self.model.fit()

    def show_and_save(self, forecast):
        pd.concat([self.__data, forecast], axis=1).plot()
        plt.savefig('graph-{}.pdf'.format(forecast.index[0]))
        plt.show()

    def predict(self, horizon, sample_frequency):
        future_forecast = self.results.predict(n_periods=horizon)

        future_ts = [v + pd.to_timedelta(sample_frequency * (i + 1), unit='s')
                     for i, v in enumerate([self.__data.index[-1]]*horizon)]
        # This returns an array of predictions:

        future_forecast = pd.DataFrame(future_forecast, index=future_ts, columns=['Prediction'])

        self.show_and_save(future_forecast)

        return future_forecast
