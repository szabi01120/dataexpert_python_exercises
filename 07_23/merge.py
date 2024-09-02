nums1 = [0]
m = 0
nums2 = [1]
n = 1

for j in range(n):
    nums1[m + j] = nums2[j]
nums1.sort()
print(nums1)