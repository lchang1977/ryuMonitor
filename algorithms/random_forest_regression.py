import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler

'''
Non linear and non continuous regression model
Lot more steps compared to decision tree
'''


class RandomForest:

    def __init__(self, features, output):
        self.regressor = None
        # x includes the features, as matrix, e.g. #bathroom, sq.feet, ...
        self.X = features
        # y is the value to predict
        self.y = output

        # splitting the dataset into the Training set and Test set
        '''from sklearn.model_selection import train_test_split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        # Feature scaling
        self.sc_X = StandardScaler()
        self.sc_y = StandardScaler()
        self.X = self.sc_X.fit_transform(self.X)
        self.y = self.sc_y.fit_transform(self.y)'''

    def fit(self):
        # Fitting Decision Tree Regression to the dataset
        # Choose the best number of tree
        self.regressor = RandomForestRegressor(n_estimators=10, random_state=0)

        # lin_reg.fit(self.X_train, self.y_test)
        self.regressor.fit(self.X, self.y)

    def show_(self):
        # Visualizing the Decision Tree Regression results
        X_grid = np.arange(min(self.X), max(self.X), 0.01)
        X_grid = X_grid.reshape((len(X_grid), 1))
        plt.scatter(self.X, self.y, color='red')
        plt.plot(X_grid, self.regressor.predict(X_grid), color='blue')
        plt.title('Truth or Bluff (Random Forest Regression)')
        plt.xlabel('Position level')
        plt.ylabel('Salary')
        plt.show()

    # to find the best model and the best parameters
    def grid_search(self):
        parameters = [{'n_estimators': [10, 50, 70, 100, 200], 'random_state': [0, 1, 2, None]}
                      ]
        grid_search = GridSearchCV(estimator=self.regressor,
                                   param_grid=parameters,
                                   cv=10,
                                   n_jobs=-1)
        grid_search = grid_search.fit(self.X, self.y)
        best_accuracy = grid_search.best_score_
        print('Accuracy : {}'.format(best_accuracy))
        best_parameters = grid_search.best_params_
        print('Parameters : {}'.format(best_parameters))
        self.regressor = grid_search

    def predict(self, value=6.5):
        return self.regressor.predict(value)
