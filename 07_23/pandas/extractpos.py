import numpy as np
import pandas as pd

ser = pd.Series(list('abcdefghijklmnopqrstuvwxyz'))
pos = [0, 4, 8, 14, 20]

ser = ser.take(pos)

print(ser)