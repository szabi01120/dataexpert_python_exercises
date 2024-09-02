nums = [1,2,3,4,5]
k = 3

count = 0
nums = sorted(nums, reverse=True)
for i in range(k):
    count += nums[0]
    nums[0] += 1
print(count)