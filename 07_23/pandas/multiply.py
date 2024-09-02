import numpy as np
import pandas as pd

ser = pd.Series(np.random.randint(1, 10, 7))

print(ser)
print("--------------")

ser = np.argwhere(ser % 3 == 0)
print(ser)