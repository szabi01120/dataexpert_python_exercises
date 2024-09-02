# labirintus előre megrajzolt pályán

def print_maze(maze):
    for row in maze:
        print(' '.join(row))
        
def is_valid_move(maze, x, y):
    if x < 0 or x >= len(maze):
        return False
    if y < 0 or y >= len(maze[0]):
        return False
    if maze[x][y] == '#':
        return False
    return True

def find_start(maze):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                return i, j
            
# def find_end(maze):
#     for i in range(len(maze)):
#         for j in range(len(maze[0])):
#             if maze[i][j] == 'C':
#                 return i, j
            
def solve_maze(maze, x, y):
    if not is_valid_move(maze, x, y):
        return False
    if maze[x][y] == 'C':
        return True
    if maze[x][y] == '#':
        return False
    maze[x][y] = 'X'
    
    if solve_maze(maze, x + 1, y):
        return True
    if solve_maze(maze, x - 1, y):
        return True
    if solve_maze(maze, x, y + 1):
        return True
    if solve_maze(maze, x, y - 1):
        return True
    
    maze[x][y] = ' '
    return False

def main():
    maze = [
        ['S', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', '#'],
        ['#', ' ', '#', '#', '#', '#', ' ', '#', ' ', '#'],
        ['#', ' ', '#', ' ', ' ', '#', ' ', '#', ' ', '#'],
        ['#', ' ', '#', ' ', '#', '#', ' ', '#', ' ', '#'],
        ['#', ' ', '#', ' ', ' ', ' ', ' ', '#', ' ', '#'],
        ['#', ' ', '#', '#', '#', '#', '#', '#', ' ', '#'],
        ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'C', '#']
    ]
    start_x, start_y = find_start(maze)
    print_maze(maze)
    print()
    if solve_maze(maze, start_x, start_y):
        print_maze(maze)
        print("Solved!")
    else:
        print("No solution")
    

if __name__ == '__main__':
    main()
