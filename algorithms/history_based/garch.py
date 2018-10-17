import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from arch import arch_model


class Garch:

    def __init__(self, data):
        self.__data = data
        self.model = {}
        self.res = []
        self.train = []
        self.test = []

        # print(data.head())

        # Interpret index as timestamp
        self.__data.index = pd.to_datetime(self.__data.index)

        # Rename column
        self.__data.columns = ['BW']

    def fit(self):
        # Find the best ARIMA fit
        '''res_tup = self._get_best_model(self.__data)
        order = res_tup[1]
        model = res_tup[2]

        # now that we have our ARIMA fit, we feed this to GARCH model
        p_ = order[0]
        o_ = order[1]
        q_ = order[2]

        self.train = model.resid[:train_size]
        self.test = model.resid[train_size:]

        self.model = arch_model(self.train, p=p_, o=o_, q=q_)
        self.res = self.model.fit(disp='off')
        print(self.res.summary())'''
        am = arch_model(self.__data)

        self.res = am.fit(disp='off')
        # print(self.res.summary())

    def predict(self, sample_frequency):
        forecasts = self.res.forecast(horizon=3, start=None, align='origin')

        future_ts = [self.__data.index[-1] + pd.to_timedelta(sample_frequency, unit='s')]
        # future_forecast = pd.DataFrame(forecasts, index=self.test.index, columns=['Prediction'])
        future_forecast = pd.DataFrame(forecasts.mean.iloc[-1, 0], index=future_ts, columns=['Prediction'])

        return future_forecast

    def _predict_var_gar(self, values):
        garch11 = arch_model(values, p=1, q=1)
        results = garch11.fit(update_freq=10)

        print(results.summary())
        forecasts = results.forecast(horizon=30, method='simulation')
        sims = forecasts.simulations

        lines = plt.plot(sims.values[-1, ::30].T, alpha=0.33)
        lines[0].set_label('Simulated paths')
        plt.plot()

        print('Percentile')
        print(np.percentile(sims.values[-1, 30].T, 5))
        plt.hist(sims.values[-1, 30], bins=50)
        plt.title('Distribution of Returns')

        # plt.show()
