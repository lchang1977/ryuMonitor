import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


class Regression:

    def __init__(self, features, output):
        self.lin_reg = None
        self.lin_reg_2 = None
        self.poly_reg = None
        # x includes the features, as matrix, e.g. #bathroom, sq.feet, ...
        self.X = features
        # y is the value to predict
        self.y = output

        # splitting the dataset into the Training set and Test set
        '''from sklearn.model_selection import train_test_split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        '''

    def linear_fit(self):
        # Fitting Linear Regression to the dataset
        self.lin_reg = LinearRegression()

        # lin_reg.fit(self.X_train, self.y_test)
        self.lin_reg.fit(self.X, self.y)

    def fit(self):
        # Fitting Polynomial Regression to the dataset
        self.poly_reg = PolynomialFeatures(degree=4)

        # X_poly = poly_reg.fit_transform(self.X_train)
        X_poly = self.poly_reg.fit_transform(self.X)
        self.poly_reg.fit(X_poly, self.y)

        self.lin_reg_2 = LinearRegression()
        self.lin_reg_2.fit(X_poly, self.y)

    def show_linear(self):
        # Visualizing the Linear Regression results
        plt.scatter(self.X, self.y, color='red')
        plt.plot(self.X, self.lin_reg.predict(self.X), color='blue')
        plt.title('Truth or Bluff (Linear Regression)')
        plt.xlabel('Position level')
        plt.ylabel('Salary')
        plt.show()

    def show_polynomial(self):
        # Visualizing the Polynomial Regression results
        X_grid = np.arange(min(self.X), max(self.X), 0.1)
        X_grid = X_grid.reshape((len(X_grid), 1))
        plt.scatter(self.X, self.y, color='red')
        # We don't use X_poly, so this block of code ,ca ne generalized changing data to show
        plt.plot(X_grid, self.lin_reg_2.predict(self.poly_reg.fit_transform(X_grid)), color='blue')
        plt.title('Truth or Bluff (Polynomial Regression)')
        plt.xlabel('Position level')
        plt.ylabel('Salary')
        plt.show()

    def linear_predict(self, value=6.5):
        return self.lin_reg.predict(value)

    def predict(self, value=6.5):
        return self.lin_reg_2.predict(self.poly_reg.fit_transform(value))
