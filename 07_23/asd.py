digits = [1,2,3]

a = ""
for i in range(len(digits)):
    a += str(digits[i])
tmp = int(a) + 1

b = [int(i) for i in str(tmp)]

print(b)