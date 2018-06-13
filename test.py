import pandas as pd
import numpy as np
from arima import Arima
from prediction import Model

data1 = pd.read_csv("electric_Production.csv", index_col=0)
arima = Arima(data1)
#arima.fit()
#arima.predict()

"""ori = np.array([('2018-06-13 06:57:01.742172', 132),
       ('2018-06-13 06:57:11.742813', 133),
       ('2018-06-13 06:57:21.743336', 2257),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
('2018-06-13 06:57:11.742813', 133),
       ('2018-06-13 06:57:31.743824', 251)])

#data = pd.DataFrame(data=ori[:, 1:], index=ori[:, 0], columns=['BW'])
data = pd.DataFrame(data=[], columns=['BW'])

# Interpret index as timestamp
data.index = pd.to_datetime(data.index)
print(data)

new = np.array([pd.to_datetime('2018-06-13 06:57:41.744592'), 119])
newD = pd.DataFrame(data=[119], index=['2018-06-13 06:57:41.744592'], columns=['BW'])
data = data.append(newD)
print(data)

# Interpret index as timestamp
data1.index = pd.to_datetime(data1.index)

# Rename column
data1.columns = ['Energy Production']

model = Model(data)
model.fit()
'''data = data.append(pd.DataFrame(['2018-06-13 06:57:41.744592', 119]))
print(data)
#data = pd.Series(ori[1], index=ori[0])
#print(data)

arima.fit_with_garch(300)
arima.predict_with_garch()'''
"""