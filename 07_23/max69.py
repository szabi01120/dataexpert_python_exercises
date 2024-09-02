num = 9669

numList = [x for x in str(num)]
for i in range(len(numList)):
    if numList[i] == '6':
        numList[i] = '9'
        break
result = int(''.join(numList))
print(result)