import numpy as np
import pandas as pd
from algorithms.history_based import arima, sarima, holt_winters, garch
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def load_data():
    values = pd.read_csv("new_test/history-2-5.csv")
    # values.index = pd.to_datetime(values.index)
    values.set_index('time')
    print(values.head())
    return values


def holt_test(train, test):
    method = holt_winters.HoltWinters(train)
    method.fit()
    output_predicted = method.predict(6, 6)
    mse = mean_squared_error(test, output_predicted)
    print('Holt Winters MSE : {}'.format(mse))
    return mse


def arima_test(train, test):
    method = arima.Arima(train)
    method.fit()
    output_predicted, deviation = method.predict(6, 6)
    mse = mean_squared_error(test, output_predicted)
    print('Arima MSE : {}'.format(mse))
    return mse


def sarima_test(train, test):
    method = sarima.Sarima(train, False)
    method.fit()
    output_predicted, deviation = method.predict(6, 6)
    mse = mean_squared_error(test, output_predicted)
    print('sArima MSE : {}'.format(mse))
    return mse


def garch_test(train, test):
    method = garch.Garch(train)
    method.fit()
    output_predicted, deviation = method.predict(6)
    mse = mean_squared_error(test, output_predicted)
    print('Garch MSE : {}'.format(mse))
    return mse


if __name__ == "__main__":
    data = load_data()
    # plot_values(data)
    # plot_bytes_sw(data)
    # plot_packets(data)
    data_train, data_test = train_test_split(data, test_size=0.2, random_state=0)
    holt_test(data_train, data_test)
    arima_test(data_train, data_test)
    sarima_test(data_train, data_test)
    garch_test(data_train, data_test)
