import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import itertools
import warnings
import sys
from pyramid.arima import auto_arima
from statsmodels.tsa.arima_model import ARIMA


class Arima:

    def __init__(self, data):
        data = data.astype(float)
        self.__data = data
        self.model = {}
        self.results = []
        print(self.__data.head())
        plt.plot(self.__data)
        # self.__data.plot()
        plt.show()

    def fit(self):
        warnings.filterwarnings("ignore")  # specify to ignore warning messages

        print('Size {}'.format(len(self.__data)))
        # Define the p, d and q parameters to take any value between 0 and 2
        p = d = q = range(0, 3)
        best_aic = sys.float_info.max

        # Generate all different combinations of p, q and q triplets
        pdq = list(itertools.product(p, d, q))

        for param in pdq:
            try:
                mod = ARIMA(self.__data, order=param)

                res = mod.fit(disp=0)
                print('ARIMA{} - AIC:{}'.format(param, res.aic))
                if res.aic < best_aic:
                    best_aic = res.aic
                    self.model = mod
            except:
                continue

        print('Best found AIC: %f' % best_aic)

        # self.train = self.__data.loc['1985-01-01':'2016-12-01']
        # self.test = self.__data.loc['2015-01-01':]

        self.results = self.model.fit(disp=0)

    def show_and_save(self, forecast):
        pd.concat([self.__data, forecast], axis=1).plot()
        plt.savefig('graph-{}.pdf'.format(forecast.index[0]))
        plt.show()

    def save_aic(self, start_ts, last_ts, line):
        with open("past-aic.txt", "a") as file:
            file.write('{}-{} :'.format(start_ts, last_ts))
            file.write(line + '\n')

    def predict(self, horizon, sample_frequency):
        future_forecast = self.results.forecast(steps=horizon)

        future_ts = [v + pd.to_timedelta(sample_frequency * (i + 1), unit='s')
                     for i, v in enumerate([self.__data.index[-1]] * horizon)]
        # This returns an array of predictions:

        print(future_forecast)

        future_forecast = pd.DataFrame(future_forecast[0], index=future_ts, columns=['Prediction'])

        self.show_and_save(future_forecast)

        return future_forecast
