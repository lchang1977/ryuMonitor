import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from evaluate import Measure

import csv
import datetime

data = pd.read_csv("band.csv", index_col=0)
data.index = pd.to_datetime(data.index)
evaluation = Measure()
evaluation.compare_cdf()


'''
test = data[:150]

# Plot ACF:
lag_acf = acf(test, nlags=20)
#plt.subplot(121)
plt.plot(lag_acf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96 / np.sqrt(len(test)), linestyle='--', color='gray')
plt.axhline(y=1.96 / np.sqrt(len(test)), linestyle='--', color='gray')
#plt.title('Autocorrelation Function')

ax.set_ylabel('Autocorrelation')
ax.set_xlabel('Lag')

fig.set_size_inches(width, height)
fig.savefig('auto.pdf')

# Plot PACF:
lag_pacf = pacf(test, nlags=20, method='ols')
#plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0, linestyle='--', color='gray')
plt.axhline(y=-1.96 / np.sqrt(len(test)), linestyle='--', color='gray')
plt.axhline(y=1.96 / np.sqrt(len(test)), linestyle='--', color='gray')
#plt.title('Partial Autocorrelation Function')

ax.set_ylabel('Partial Autocorrelation')
ax.set_xlabel('Lag')

fig.set_size_inches(width, height)
fig.savefig('partial auto.pdf')

'''

