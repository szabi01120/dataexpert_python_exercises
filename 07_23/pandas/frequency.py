import numpy as np
import pandas as pd

ser = pd.Series(np.take(list('abcdefgh'), np.random.randint(8, size=30)))

result = ser.value_counts()

print(result)