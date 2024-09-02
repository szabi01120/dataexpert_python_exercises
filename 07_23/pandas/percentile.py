import numpy as np
import pandas as pd

state = np.random.RandomState(100)
ser = pd.Series(state.normal(10, 5, 25))

result = np.percentile(ser, q=[0, 25, 50, 75, 100])

print(result)