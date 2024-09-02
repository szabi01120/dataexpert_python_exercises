import numpy as np
import pandas as pd

ser1 = pd.Series(list('abcedfghijklmnopqrstuvwxyz'))
ser2 = pd.Series(np.arange(26))
df = pd.merge(ser1.to_frame(), ser2.to_frame(), left_index=True, right_index=True, suffixes=('_left', '_right'))

print(df.head())
