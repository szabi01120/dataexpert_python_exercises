def main():
    nums = [8]

    count = 0
    
    if len(nums) == 1:
        return print(count)
    for i in range(len(nums) - 1):
        if nums[i + 1] < nums[i]:
            while nums[i + 1] != nums[i] + 1:
                nums[i + 1] += 1
                count += 1
    return print(count)
    
if __name__ == "__main__":
    main()