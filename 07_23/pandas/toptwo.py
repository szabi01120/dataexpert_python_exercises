import numpy as np
import pandas as pd

state = np.random.RandomState(100)
ser = pd.Series(np.random.randint(1, 5, [12]))

print("top 2 freq:", ser.value_counts())
ser[~ser.isin(ser.value_counts().index[:2])] = "other"

print(ser)