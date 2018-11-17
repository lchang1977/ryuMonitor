import numpy as np
import pandas as pd
from algorithms import svr
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


def load_data():
    values = pd.read_csv("new_test/history-2-5.csv")
    switch = pd.read_csv("new_test/switch-2.csv")
    flows = pd.read_csv("new_test/flows-2.csv")
    # values.index = pd.to_datetime(values.index)
    values = values.assign(pkt_swtch=switch['packets'], bytes_swtch=switch['bytes'], bytes_flow=flows['bytes'])
    values.set_index('time')
    print(values.head())
    return values


def svr_test(features_train, features_test, output_train, output_test):
    method = svr.Svr(features_train, output_train)
    method.fit()
    output_predicted = method.predict(features_test)
    mse = mean_squared_error(output_test, output_predicted)
    print('SVR MSE : {}'.format(mse))
    return mse


def gpr_test(features_train, features_test, output_train, output_test):
    method = svr.Svr(features_train, output_train)
    method.fit()
    output_predicted = method.predict(features_test)
    mse = mean_squared_error(output_test, output_predicted)
    print('SVR MSE : {}'.format(mse))
    return mse

if __name__ == "__main__":
    data = load_data()
    # plot_values(data)
    # plot_bytes_sw(data)
    # plot_packets(data)
    features = data.iloc[:, 2:4].values
    output = data['BW'].values
    features_train, features_test, output_train, output_test = train_test_split(features, output,
                                                                                test_size=0.2, random_state=0)
    svr_test(features_train, features_test, output_train, output_test)
