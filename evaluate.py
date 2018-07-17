import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA


class Measure:

    def __init__(self):
        self.forecast = pd.read_csv("pred-best.csv", index_col=0)
        # Interpret index as timestamp
        self.forecast.index = pd.to_datetime(self.forecast.index)

        self.data = pd.read_csv("band.csv", index_col=0)
        # Interpret index as timestamp
        self.data.index = pd.to_datetime(self.data.index)

        self.test = None

    def model_quality(self):
        print('d')

    def plot_error(self):
        data = self.data[151:]
        forecast = self.forecast[:-10]
        print(len(data))
        print(len(forecast))
        print(data.index[0])
        print(forecast.index[0])
        print(data.index[-1])
        print(forecast.index[-1])
        forecast = forecast['Prediction'].values
        data = data['BW'].values
        error = np.abs((data - forecast) / data)
        error = self.reject_outliers(error)
        print(((forecast - data)**2).mean())
        print(mean_squared_error(data, forecast))
        plt.plot(error)
        # error.plot()
        plt.show()

    @staticmethod
    def reject_outliers(data, m=2):
        return data[abs(data - np.mean(data)) < m * np.std(data)]

    def forecast_real(self):
        # pd.concat([self.test, future_forecast], axis=1).plot()
        pd.concat([self.data, self.forecast], axis=1).plot()
        plt.show()

    def residuals(self, model):
        # plot residual errors
        residuals = pd.DataFrame(model.resid)
        residuals.plot()
        pyplot.show()
        residuals.plot(kind='kde')
        pyplot.show()

    def diagnostics(self, model):
        results = model.fit()
        results.plot_diagnostics(figsize=(15, 12))
        plt.show()

    def dotted_value(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        npre = len(self.forecast)
        ax.set(title='Ridership', xlabel='Date', ylabel='Bandwidth')
        ax.plot(self.data.index[:], self.data.ix[:, 'bw'], 'o', label='Observed')
        ax.plot(self.data.index[:], self.data.ix[:, 'forecast'], 'g',
                label='Dynamic forecast')
        legend = ax.legend(loc='lower right')
        legend.get_frame().set_facecolor('w')
        plt.savefig('ts_predict_compare.png', bbox_inches='tight')

    def mse(self):
        error = mean_squared_error(self.test, self.forecast)
        print('Test MSE: %.3f' % error)
