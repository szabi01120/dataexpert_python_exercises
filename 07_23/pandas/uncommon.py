import pandas as pd
import numpy as np

ser1 = pd.Series([1, 2, 3, 4, 5])
ser2 = pd.Series([4, 5, 6, 7, 8])
ser_un = pd.Series(np.union1d(ser1, ser2))
ser_i = pd.Series(np.intersect1d(ser1, ser2))

ser_un = ser_un[~ser_un.isin(ser_i)]

print(ser_un)

