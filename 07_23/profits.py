prices = [7,6,4,3,1]

minn = float('inf')
maxx = 0

for i in range(len(prices)):
    if (prices[i] < minn):
        minn = prices[i]
    elif (prices[i] - minn > maxx):
        maxx = prices[i] - minn
print(maxx) 
    
    