import numpy as np
import pandas as pd
from algorithms import svr, gpr, plsr, regression, random_forest_regression, decision_tree_regression
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
    method = gpr.Gpr(features_train, output_train)
    method.fit()
    output_predicted, deviation = method.predict(features_test)
    mse = mean_squared_error(output_test, output_predicted)
    print('GPR MSE : {}'.format(mse))
    return mse


def poly_regression_test(features_train, features_test, output_train, output_test):
    method = regression.Regression(features_train, output_train)
    method.fit()
    output_predicted = method.predict(features_test)
    mse = mean_squared_error(output_test, output_predicted)
    print('Polynomial Regression MSE : {}'.format(mse))
    return mse


def linear_regression_test(features_train, features_test, output_train, output_test):
    method = regression.Regression(features_train, output_train)
    method.linear_fit()
    output_predicted = method.linear_predict(features_test)
    mse = mean_squared_error(output_test, output_predicted)
    print('Linear Regression MSE : {}'.format(mse))
    return mse


def random_forest_test(features_train, features_test, output_train, output_test):
    method = random_forest_regression.RandomForest(features_train, output_train)
    method.fit()
    output_predicted = method.predict(features_test)
    mse = mean_squared_error(output_test, output_predicted)
    print('Random Forest Regression MSE : {}'.format(mse))
    return mse


def decision_tree_test(features_train, features_test, output_train, output_test):
    method = decision_tree_regression.DecisionTree(features_train, output_train)
    method.fit()
    output_predicted = method.predict(features_test)
    mse = mean_squared_error(output_test, output_predicted)
    print('Decision Tree Regression MSE : {}'.format(mse))
    return mse


def p_least_square_test(features_train, features_test, output_train, output_test):
    method = plsr.Plsr(features_train, output_train)
    method.fit()
    output_predicted = method.predict(features_test)
    mse = mean_squared_error(output_test, output_predicted)
    print('Partial least squares Regression MSE : {}'.format(mse))
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
    poly_regression_test(features_train, features_test, output_train, output_test)
    linear_regression_test(features_train, features_test, output_train, output_test)
    random_forest_test(features_train, features_test, output_train, output_test)
    decision_tree_test(features_train, features_test, output_train, output_test)
    p_least_square_test(features_train, features_test, output_train, output_test)
    # ERROR WITH GPR!!!!!!!!!!!!
    # gpr_test(features_train, features_test, output_train, output_test)
