import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from arima import Arima
from prediction import Model

import csv
import datetime

data = pd.read_csv("band.csv", index_col=0)
data.index = pd.to_datetime(data.index)
forecast = pd.read_csv("pred.csv", index_col=0)
forecast.index = pd.to_datetime(forecast.index)
pd.concat([data, forecast], axis=1, sort=True).plot()
plt.savefig('graph-{}.pdf'.format(forecast.index[0]))
plt.show()

data1 = pd.read_csv("electric_Production.csv", index_col=0)
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
model.predict(5, 30)

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