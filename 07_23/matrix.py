grid = [[9,9,8,1],
        [5,6,2,6],
        [8,2,6,4],
        [6,2,2,2]]

maxLocal = []
tmpList = []
n = len(grid)
for i in range(0, n - 2):
    for j in range(0, n - 2):
        tmpList.append(grid[i][j])
        break
        
print(tmpList)