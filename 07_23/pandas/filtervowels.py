import pandas as pd

ser = pd.Series(['Apple', 'Orange', 'Plan', 'Python', 'Money'])
vowels = pd.Series(list('aeiou'))

duplicate = pd.Series([])

count = 0
for i in ser:
    if i.isin(vowels):
        count += 1
    if count >= 2:
        duplicate._append(i)
    count = 0

print(ser)
print(vowels)
print(duplicate)