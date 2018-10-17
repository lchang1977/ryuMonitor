import warnings
import pandas as pd
import matplotlib.pyplot as plt
from algorithms.history_based.sarima import Sarima
from algorithms.history_based.arima import Arima
from algorithms.history_based.garch import Garch
from algorithms.history_based.holt_winters import HoltWinters

plt.style.use('fivethirtyeight')


def find_best():
    data1 = pd.read_csv("band.csv", index_col=0)

    # reduce dataset
    # data1 = data1[:800]

    # Interpret index as timestamp
    data1.index = pd.to_datetime(data1.index)

    forecast = None

    for count in range(0, len(data1)-150, 15):
        training_data = data1[count:count+150]
        model = Sarima(training_data, True)
        model.fit()
        if count == 0:
            forecast = model.predict(15, 1)
        else:
            forecast = forecast.append(model.predict(15, 1))

    # save on file the predicted values
    forecast.to_csv('pred-best.csv', sep=',')

    ax = data1.plot(label='observed', figsize=(20, 15))
    forecast.plot(ax=ax, label='Forecast')
    ax.set_xlabel('Date')
    ax.set_ylabel('Bandwidth [B/s]')

    plt.legend()
    plt.show()


def find_best_no_seasonal():
    data1 = pd.read_csv("band.csv", index_col=0)

    # reduce dataset
    # data1 = data1[:800]

    # Interpret index as timestamp
    data1.index = pd.to_datetime(data1.index)

    forecast = None

    for count in range(0, len(data1)-150, 15):
        training_data = data1[count:count+150]
        model = Arima(training_data)
        model.fit()
        if count == 0:
            forecast = model.predict(15, 1)
        else:
            forecast = forecast.append(model.predict(15, 1))

    # save on file the predicted values
    forecast.to_csv('pred-best-no-s.csv', sep=',')

    ax = data1.plot(label='observed', figsize=(20, 15))
    forecast.plot(ax=ax, label='Forecast')
    ax.set_xlabel('Date')
    ax.set_ylabel('Bandwidth [B/s]')

    plt.legend()
    plt.show()


def garch():
    data1 = pd.read_csv("band.csv", index_col=0)

    # reduce dataset
    # data1 = data1[:800]

    # Interpret index as timestamp
    data1.index = pd.to_datetime(data1.index)

    forecast = None

    for count in range(0, len(data1) - 150):
        print(count)
        training_data = data1[count:count + 150]
        model = Garch(training_data)
        model.fit(150)
        if count == 0:
            forecast = model.predict(1)
        else:
            forecast = forecast.append(model.predict(1))

    # save on file the predicted values
    forecast.to_csv('pred-best-garch.csv', sep=',')
    print(forecast.head())

    ax = data1.plot(label='observed', figsize=(20, 15))
    forecast.plot(ax=ax, label='Forecast')
    ax.set_xlabel('Date')
    ax.set_ylabel('Bandwidth [B/s]')

    plt.legend()
    plt.show()


def holt_winters():
    data1 = pd.read_csv("band.csv", index_col=0)
    data1.index = pd.to_datetime(data1.index)
    forecast = None
    warnings.filterwarnings("ignore")  # specify to ignore warning messages

    for count in range(0, len(data1)-150, 15):
        training_data = data1[count:count+150]
        model = HoltWinters(training_data)
        model.fit()
        if count == 0:
            forecast = model.predict(15, 1)
        else:
            forecast = forecast.append(model.predict(15, 1))

    # save on file the predicted values
    forecast.to_csv('pred-best-holt.csv', sep=',')
    print(forecast.head())

    ax = data1.plot(label='observed', figsize=(20, 15))
    forecast.plot(ax=ax, label='Forecast')
    ax.set_xlabel('Date')
    ax.set_ylabel('Bandwidth (B/s)')

    plt.legend()
    plt.show()


# find_best()
# find_best_no_seasonal()
# garch()
holt_winters()

'''pred = results.get_prediction(start=150, dynamic=False)
pred_ci = pred.conf_int()

ax = data1[150:].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)

ax.fill_between(pred_ci.index,
                pred_ci.iloc[:, 0],
                pred_ci.iloc[:, 1], color='k', alpha=.2)

ax.set_xlabel('Date')
ax.set_ylabel('Bandwidth')
plt.legend()
plt.show()

y_forecasted = pred.predicted_mean
y_truth = data1[150:]

# Compute the mean square error
mse = mean_squared_error(y_truth, y_forecasted)
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

'''