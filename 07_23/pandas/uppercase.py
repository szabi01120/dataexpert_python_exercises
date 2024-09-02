# caoitalize and count the number of characters in a pandas series

import pandas as pd
import numpy as np

ser = pd.Series(['how', 'to', 'kick', 'ass?'])

ser = ser.str.capitalize()

count = pd.Series([len(x) for x in ser])

print(count)