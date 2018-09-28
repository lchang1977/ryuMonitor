import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import itertools
import warnings
import sys
from pyramid.arima import auto_arima
from statsmodels.tsa.arima_model import ARIMA


class Model:

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

    def fit_no_seasonal(self):
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
                if res.aic<best_aic:
                    best_aic = res.aic
                    self.model = mod
            except:
                continue

        print('Best found AIC: %f' % best_aic)

        # self.train = self.__data.loc['1985-01-01':'2016-12-01']
        # self.test = self.__data.loc['2015-01-01':]

        self.results = self.model.fit(disp=0)

    def use_best_fit(self):
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


    def save_aic(self, start_ts, last_ts, line):
        with open("past-aic.txt", "a") as file:
            file.write('{}-{} :'.format(start_ts, last_ts))
            file.write(line + '\n')

    def predict_with_best(self, horizon, sample_frequency):
        pred = self.results.get_forecast(steps=horizon)

        # Get confidence intervals of forecasts
        pred_ci = pred.conf_int()

        future_ts = [v + pd.to_timedelta(sample_frequency * (i + 1), unit='s')
                     for i, v in enumerate([self.__data.index[-1]] * horizon)]
        future_forecast = pd.DataFrame(pred.predicted_mean.values, index=future_ts, columns=['Prediction'])

        self.show_and_save(future_forecast)

        return future_forecast

    def predict(self, horizon, sample_frequency):
        future_forecast = self.model.predict(n_periods=horizon)

        future_ts = [v + pd.to_timedelta(sample_frequency * (i + 1), unit='s')
                     for i, v in enumerate([self.__data.index[-1]]*horizon)]
        # This returns an array of predictions:

        print(future_forecast)

        future_forecast = pd.DataFrame(future_forecast, index=future_ts, columns=['Prediction'])

        self.show_and_save(future_forecast)

        return future_forecast

    def predict_no_seasonal(self, horizon, sample_frequency):
        future_forecast = self.results.forecast(steps=horizon)

        future_ts = [v + pd.to_timedelta(sample_frequency * (i + 1), unit='s')
                     for i, v in enumerate([self.__data.index[-1]] * horizon)]
        # This returns an array of predictions:

        print(future_forecast)

        future_forecast = pd.DataFrame(future_forecast[0], index=future_ts, columns=['Prediction'])

        self.show_and_save(future_forecast)

        return future_forecast