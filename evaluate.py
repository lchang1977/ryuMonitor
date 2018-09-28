import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('pdf')
import matplotlib.pylab as plt
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
from pandas.plotting import autocorrelation_plot
from statsmodels.tsa.stattools import acf, pacf


class Measure:

    def __init__(self):
        self.forecast = pd.read_csv("pred-best.csv", index_col=0)
        self.forecast_no_s = pd.read_csv("pred-best-no-s.csv", index_col=0)
        self.forecast_garch = pd.read_csv("pred-best-garch.csv", index_col=0)
        self.forecast_holt = pd.read_csv("pred-best-holt.csv", index_col=0)

        self.data = pd.read_csv("band.csv", index_col=0)
        # Interpret index as timestamp
        self.data.index = pd.to_datetime(self.data.index)

        self.test = self.data[:150]

    def autocorrelation(self):
        '''
        autocorrelation_plot(test)
        plt.xlim(0, 10)
        plt.show()
        '''
        plt.rc('font', family='serif', serif='Times')
        plt.rc('text', usetex=True)
        plt.rc('xtick', labelsize=8)
        plt.rc('ytick', labelsize=8)
        plt.rc('axes', labelsize=8)

        # width as measured in inkscape
        width = 2.987
        height = width / 1.618

        fig, ax = plt.subplots()
        fig.subplots_adjust(left=.18, bottom=.19, right=.99, top=.97)

        # Plot ACF:
        lag_acf = acf(self.test, nlags=20)
        # plt.subplot(121)
        plt.plot(lag_acf)
        plt.axhline(y=0, linestyle='--', color='gray')
        plt.axhline(y=-1.96 / np.sqrt(len(self.test)), linestyle='--', color='gray')
        plt.axhline(y=1.96 / np.sqrt(len(self.test)), linestyle='--', color='gray')
        # plt.title('Autocorrelation Function')

        # ax.grid(zorder=0)

        ax.set_ylabel('Autocorrelation')
        ax.set_xlabel('Lag')

        fig.set_size_inches(width, height)
        fig.savefig('auto.pdf')

    def partial_autocorrelation(self):
        plt.rc('font', family='serif', serif='Times')
        plt.rc('text', usetex=True)
        plt.rc('xtick', labelsize=8)
        plt.rc('ytick', labelsize=8)
        plt.rc('axes', labelsize=8)

        # width as measured in inkscape
        width = 2.987
        height = width / 1.618

        fig, ax = plt.subplots()
        fig.subplots_adjust(left=.18, bottom=.19, right=.99, top=.97)

        # Plot PACF:
        lag_pacf = pacf(self.test, nlags=20, method='ols')
        # plt.subplot(122)
        plt.plot(lag_pacf)
        plt.axhline(y=0, linestyle='--', color='gray')
        plt.axhline(y=-1.96 / np.sqrt(len(self.test)), linestyle='--', color='gray')
        plt.axhline(y=1.96 / np.sqrt(len(self.test)), linestyle='--', color='gray')
        # plt.title('Partial Autocorrelation Function')

        # ax.grid(zorder=0)

        ax.set_ylabel('Partial Autocorrelation')
        ax.set_xlabel('Lag')

        fig.set_size_inches(width, height)
        fig.savefig('partial.pdf')

    def compare_cdf(self):
        # width as measured in inkscape
        width = 3.987
        height = width / 1.618

        fig, ax = plt.subplots()
        fig.subplots_adjust(left=.15, bottom=.19, right=.98, top=.97)

        data = self.data[151:]
        forecast = self.forecast[:-10]
        forecast_no_s = self.forecast_no_s[1:-9]
        forecast_garch = self.forecast_garch[1:]
        forecast_holt = self.forecast_holt[1:-9]
        print(len(data))
        print(len(forecast))
        print(len(forecast_no_s))
        print(len(forecast_garch))
        print(len(forecast_holt))
        print(data.index[0])
        print(forecast.index[0])
        print(forecast_no_s.index[0])
        print(forecast_garch.index[0])
        print(forecast_holt.index[0])
        print(data.index[-1])
        print(forecast.index[-1])
        print(forecast_no_s.index[-1])
        print(forecast_garch.index[-1])
        print(forecast_holt.index[-1])
        forecast = forecast['Prediction'].values
        forecast_no_s = forecast_no_s['Prediction'].values
        forecast_garch = forecast_garch['Prediction'].values
        forecast_holt = forecast_holt['Prediction'].values
        data = data['BW'].values
        error = np.abs((data - forecast) / data)
        error_no_s = np.abs((data - forecast_no_s) / data)
        error_garch = np.abs((data - forecast_garch) / data)
        error_holt = np.abs((data - forecast_holt) / data)
        # error = self.reject_outliers(error)

        x = np.sort(error)
        y = np.arange(1, len(x) + 1) / len(x)
        x1 = np.sort(error_no_s)
        y1 = np.arange(1, len(x1) + 1) / len(x1)
        x2 = np.sort(error_holt)
        y2 = np.arange(1, len(x2) + 1) / len(x2)
        x3 = np.sort(error_garch)
        y3 = np.arange(1, len(x3) + 1) / len(x3)
        # _ = plt.plot(x, y, marker='.', linestyle='None')
        _ = plt.plot(x, y)
        _ = plt.plot(x1, y1, linestyle='--')
        _ = plt.plot(x2, y2, linestyle=':')
        # _ = plt.plot(x3, y3, linestyle='-.')
        ax.set_xlabel('Relative Error of Bandwidth Prediction')
        ax.set_ylabel('CDF')
        plt.legend(('SARIMA', 'ARIMA', 'Holt-Winters', 'GARCH'), loc='lower right')
        plt.margins(0.02)

        fig.set_size_inches(width, height)
        fig.savefig('cdf_new.pdf')

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
