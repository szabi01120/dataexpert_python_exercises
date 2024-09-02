import numpy as np
import pandas as pd

ser = pd.Series(np.random.random(20))

res = pd.qcut(ser, q=[0, .10, .20, .30, .40, .50, .60, .70, .80, .90, 1], \
        labels=['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th'])

res2 = pd.qcut(range(5), 4)
print(ser)
print("----------------------")
print(res)