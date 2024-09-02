import pandas as pd
from dateutil.parser import parse

ser = pd.Series(['Jan 2010', 'Feb 2011', 'Mar 2012'])

ser = ser.map(lambda x: parse('04' + x))
print(ser)