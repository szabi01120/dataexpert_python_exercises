candies = [2,3,5,1,3]
extraCandies = 3

rList = []
for i in range(len(candies)):
    candies[i] += extraCandies
    rList.append(True) if max(candies) == candies[i] else rList.append(False)
    candies[i] -= extraCandies
print(rList)