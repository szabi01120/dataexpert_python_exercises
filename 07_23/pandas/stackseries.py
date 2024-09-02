import pandas as pd
import numpy as np

ser1 = pd.Series(range(5))
ser2 = pd.Series(list('abcde'))

ser1._append(ser2)

df = pd.concat([ser1, ser2], axis=1, keys=['ser1', 'ser2'])
print(df)