import pandas as pd
import numpy as np
import itertools
import warnings
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
from prediction import Model
from evaluate import Measure

import csv
import datetime

evaluation = Measure()
# evaluation.plot_error()
# evaluation.ecdf_error()
evaluation.compare_cdf()
# evaluation.plot_forecast()
# evaluation.histogram_error()

'''
plt.style.use('fivethirtyeight')

data = pd.read_csv("band.csv", index_col=0)
#data = data[202:]
data.index = pd.to_datetime(data.index)
forecast = pd.read_csv("pred.csv", index_col=0)
#forecast = forecast[140:]
forecast.index = pd.to_datetime(forecast.index)
#pd.concat([data, forecast], axis=1, sort=True).plot()
plt.plot(data)
plt.plot(forecast, color='red')
plt.savefig('graph-{}.pdf'.format(forecast.index[0]))
plt.show()

ax = data.plot(label='observed', figsize=(20, 15))
forecast.plot(ax=ax, label='Forecast')
ax.set_xlabel('Date')
ax.set_ylabel('Bandwidth [B/s]')

plt.legend()
plt.show()

arima = Model(data, False)
# comment out here for choosing best params
arima.fit()

# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
mod = sm.tsa.statespace.SARIMAX(data,
                                order=(1, 0, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit(disp=0)
print('ARIMA AIC:{}'.format(results.aic))
print(results.summary().tables[1])

mod = sm.tsa.statespace.SARIMAX(data,
                                order=(0, 0, 1),
                                seasonal_order=(1, 1, 1, 12),
                                enforce_stationarity=False,
                                enforce_invertibility=False)
results = mod.fit(disp=0)
print('ARIMA AIC:{}'.format(results.aic))
print(results.summary().tables[1])'''

'''warnings.filterwarnings("ignore") # specify to ignore warning messages

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(data,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

            results = mod.fit(disp=0)

            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            with open("results.txt", "a") as file:
                file.write('ARIMA{}x{}12 - AIC:{} \n'.format(param, param_seasonal, results.aic))
                file.write(str(results.summary().tables[1]) + '\n')
        except:
            continue
'''
# results.plot_diagnostics(figsize=(15, 12))
plt.show()

"""data1 = pd.read_csv("electric_Production.csv", index_col=0)
# Interpret index as timestamp
data1.index = pd.to_datetime(data1.index)

# Rename column
data1.columns = ['Energy Production']
arima = Arima(data1)
#arima.fit()
#arima.predict()

ori = np.array([('2018-06-13 06:57:01.742172', 132.23),
                ('2018-06-13 06:57:11.742812', 133.32),
                ('2018-06-13 06:57:21.743336', 2257.68),
                ('2018-06-13 06:57:11.742813', 133.3),
                ('2018-06-13 06:57:11.742814', 133.2),
                ('2018-06-13 06:57:11.742815', 133.9),
                ('2018-06-13 06:57:11.742816', 133.1),
                ('2018-06-13 06:57:11.742817', 133.1),
                ('2018-06-13 06:57:11.742818', 133.02),
                ('2018-06-13 06:57:11.742819', 133.05),
                ('2018-06-13 06:57:11.742820', 133.0),
                ('2018-06-13 06:57:11.742821', 133.31),
                ('2018-06-13 06:57:11.742822', 133.98),
                ('2018-06-13 06:57:11.742823', 133.42),
                ('2018-06-13 06:57:11.742824', 133.42),
                ('2018-06-13 06:57:11.742825', 133.42),
                ('2018-06-13 06:57:31.743826', 251)])

data = pd.DataFrame(data=ori[:, 1:], index=ori[:, 0], columns=['BW'])
data.index = pd.to_datetime(data.index)

#data.plot()
#plt.plot(ori)
#plt.show()

model = Model(data)
model.fit()
model.predict(5, 30)"""

"""

#data = pd.DataFrame(data=ori[:, 1:], index=ori[:, 0], columns=['BW'])
data = pd.DataFrame(data=[], columns=['BW'])

# Interpret index as timestamp
data.index = pd.to_datetime(data.index)
print(data)


model = Model(data)
model.fit()
'''data = data.append(pd.DataFrame(['2018-06-13 06:57:41.744592', 119]))
print(data)
#data = pd.Series(ori[1], index=ori[0])
#print(data)

arima.fit_with_garch(300)
arima.predict_with_garch()'''
"""