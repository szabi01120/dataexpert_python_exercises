# Tic-tac-toe a gép ellen: X és O felváltva, 3x3 pályán. Előny ha gép nem teljesen buta.
import random

boxes = [ '_', '_', '_',
          '_', '_', '_',
          '_', '_', '_' ]
HUMAN = 'X'
COMPUTER = 'O'
WINNER_CHOICES = [ [0, 1, 2], [3, 4, 5], [6, 7, 8],
                   [0, 3, 6], [1, 4, 7], [2, 5, 8],
                   [0, 4, 8], [2, 4, 6] ]

def screener(initial=False):
    board = '''
             {} | {} | {} 
            -----------
             {} | {} | {}
            -----------
             {} | {} | {} 
        '''.format(*([x for x in range(1, 10)] if initial else boxes))
    print(board)
    
def player_move():
    while True:
        try:
            move = int(input("Enter your move (1-9): "))
            if move not in range(1, 10):
                print("Invalid move")
                continue
            if boxes[move - 1] != '_':
                print("That box is already taken")
                continue
            boxes[move - 1] = HUMAN
            break
        except ValueError:
            print("Please enter a VALID number in the range 1-9")
    return winner_check() == HUMAN
    
def computer_move():   
    if boxes[4] == '_':
        boxes[4] = COMPUTER
        return False
    
    for choice in WINNER_CHOICES:
        comp_count = 0
        human_count = 0
        for i in choice:
            if boxes[i] == COMPUTER:
                comp_count += 1
            elif boxes[i] == HUMAN:
                human_count += 1
            else:
                empty = i
        if comp_count == 2 and human_count == 0:
            boxes[empty] = COMPUTER
            return True
        elif human_count == 2 and comp_count == 0:
            boxes[empty] = COMPUTER
            if winner_check() == COMPUTER:
                return True
            return False
        
    move = random.choice([i for i, box in enumerate(boxes) if box == '_' and i in [0, 2, 6, 8]])
    boxes[move] = COMPUTER
    return False    
    
def winner_check():
    for choices in WINNER_CHOICES:
        if boxes[choices[0]] == boxes[choices[1]] == boxes[choices[2]] != '_':
            return boxes[choices[0]]

def main():
    player_won = False
    computer_won = False
    while player_won is False and computer_won is False:
        print("-------------Tic-tac-toe-------------")
        screener()
        print("-------------Tic-tac-toe-------------")
        player_won = player_move()
        
        if '_' not in boxes:
            screener()
            print("It's a tie!")
            break
        computer_won = computer_move()
        if player_won:
            screener()
            print("Player won!")
            break
        elif computer_won:
            screener()
            print("Computer won!")
            break        

if __name__ == '__main__':
    main()