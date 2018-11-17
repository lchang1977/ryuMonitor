import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cross_decomposition import PLSRegression
from sklearn.preprocessing import StandardScaler


# Partial least squares regression (PLS regression)
class Plsr:

    def __init__(self, features, output):
        self.regressor = None
        # x includes the features, as matrix, e.g. #bathroom, sq.feet, ...
        self.X = features
        # y is the value to predict
        self.y = output

        # splitting the dataset into the Training set and Test set
        '''from sklearn.model_selection import train_test_split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=0)'''

        # Feature scaling
        self.sc_X = StandardScaler()
        self.sc_y = StandardScaler()
        self.X = self.sc_X.fit_transform(self.X)
        self.y = self.sc_y.fit_transform(self.y)

    def fit(self):
        # Fitting Partial Least Squares Regression to the dataset
        self.regressor = PLSRegression(n_components=1)

        # lin_reg.fit(self.X_train, self.y_test)
        self.regressor.fit(self.X, self.y)

    def show_(self):
        # Visualizing the Partial Least Squares Regression results
        X_grid = np.arange(min(self.X), max(self.X), 0.1)
        X_grid = X_grid.reshape((len(X_grid), 1))
        plt.scatter(self.X, self.y, color='red')
        # We don't use X_poly, so this block of code ,ca ne generalized changing data to show
        plt.plot(X_grid, self.regressor.predict(X_grid), color='blue')
        plt.title('Truth or Bluff (PLSR Model)')
        plt.xlabel('Position level')
        plt.ylabel('Salary')
        plt.show()

    def predict(self, value=6.5):
        y_pred = self.regressor.predict(self.sc_X.transform(np.array([[value]])))
        return self.sc_y.inverse_transform(y_pred)
