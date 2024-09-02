import pandas as pd

ser = pd.Series([1, 3, 6, 10, 15, 21, 27, 35])

ser2 = ser.diff().tolist()

print(ser2)
print(ser.diff().diff().tolist())
