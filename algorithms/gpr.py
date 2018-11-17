import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C


class Gpr:

    def __init__(self, features, output):
        self.gp = None
        # x includes the features, as matrix, e.g. #bathroom, sq.feet, ...
        self.X = features
        # y is the value to predict
        self.y = output

        # splitting the dataset into the Training set and Test set
        '''from sklearn.model_selection import train_test_split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=0)'''

    def fit(self):
        # Instantiate a Gaussian Process model
        kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
        self.gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)

        # Fit to data using Maximum Likelihood Estimation of the parameters
        self.gp.fit(self.X, self.y)

    def show_(self):
        # Mesh the input space for evaluations of the real function, the prediction and
        # its MSE
        x = np.atleast_2d(np.linspace(0, 10, 1000)).T
        y_pred, sigma = self.predict(x)
        # Plot the function, the prediction and the 95% confidence interval based on
        # the MSE
        plt.figure()
        plt.plot(self.X, self.y, 'r.', markersize=10, label=u'Observations')
        plt.plot(x, y_pred, 'b-', label=u'Prediction')
        plt.fill(np.concatenate([self.X, x[::-1]]),
                 np.concatenate([y_pred - 1.9600 * sigma,
                                 (y_pred + 1.9600 * sigma)[::-1]]),
                 alpha=.5, fc='b', ec='None', label='95% confidence interval')
        plt.xlabel('$x$')
        plt.ylabel('$f(x)$')
        plt.ylim(-10, 20)
        plt.legend(loc='upper left')

        plt.show()

    def predict(self, value=6.5):
        # Make the prediction on the meshed x-axis (ask for MSE as well)
        y_pred, sigma = self.gp.predict(value, return_std=True)
        return y_pred, sigma
