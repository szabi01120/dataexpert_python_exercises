import numpy as np
import pandas as pd

mylist = list('abcedfghijklmnopqrstuvwxyz')
myarr = np.arange(26)
mydict = dict(zip(mylist, myarr))
ser = pd.Series(mydict)
ser.name = 'alphabets'
dtframe = ser.to_frame().reset_index()

print(dtframe.head())