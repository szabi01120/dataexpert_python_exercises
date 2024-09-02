import numpy as np
import pandas as pd

ser = pd.Series(np.random.randint(1, 10, 35))

ser = pd.DataFrame(ser.values.reshape(7,5))
print(ser)