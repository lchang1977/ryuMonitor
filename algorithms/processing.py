import numpy as np
import pandas as pd
import datetime as dt
from datetime import timezone

from sklearn.preprocessing import StandardScaler


class Processing:

    def __init__(self):
        self.scaler = None

    def scale_train_date(self, dates):
        # dates as Series, in form 'YYYY-MM-DD'
        ''' Dovrei considerare bene se il test set considerarlo per il fit, perché lo scale consiste nello scalare i
        dati in modo da avere una gaussiana con media 0 e dev.std. 1'''

        timestamps = dates.apply(lambda v: v.replace(tzinfo=timezone.utc).timestamp())
        self.scaler = StandardScaler()
        return self.scaler.fit_transform(timestamps[:, np.newaxis])

    def scale_test_date(self, dates):
        # dates as Series, in form 'YYYY-MM-DD'

        timestamps = dates.apply(lambda v: v.replace(tzinfo=timezone.utc).timestamp())
        x = np.array(timestamps)
        return self.scaler.transform(x.reshape(1, -1))
