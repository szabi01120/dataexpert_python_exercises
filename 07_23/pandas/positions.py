# 16. How to get the positions of items of series A in another series B?

import pandas as pd
import numpy as np

ser1 = pd.Series([10, 9, 6, 5, 3, 1, 12, 8, 13])
ser2 = pd.Series([1, 3, 10, 13])

print([np.where(i == ser1)[0].tolist()[0] for i in ser2])
