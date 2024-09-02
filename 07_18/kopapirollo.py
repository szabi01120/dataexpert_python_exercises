import random

def scoreboard(score):
    print()
    print("========SCOREBOARD========")
    print("Számítógép: ", score["computer"])
    print("Játékos: ", score["player"])
    print("Döntetlen: ", score["draw"])
    print("==========================")
    print()

def comp_choice():
    return random.randint(1, 3)

def player_choice(choice):
    choice_mapper = {
        "kő": 1,
        "papír": 2,
        "olló": 3
    }
    if not choice in choice_mapper.keys():
        return None
    return choice_mapper[choice]

def decide(player, computer):
    choice_index = [1, 2, 3, 1]
    if player == computer:
        return 0,0,1
    
    if computer == choice_index[player]:
        return 0,1,0
    return 1,0,0
    
def main():
    score = {"player": 0, "computer": 0, "draw": 0}
    while True:
        player = input("Kilépéshez írd be azt, hogy 'exit'!\nKő, papír vagy olló? ")
        
        if player.lower() == "exit":
            return False
        
        if player_choice(player) == None:
            print("Kérlek válassz az alábbi 3 lehetőség közül: kő, papír, olló")
            continue
        
        player_asd = player_choice(player)
        computer = comp_choice()        
        print(computer)
        print(player_asd)
        
        result = decide(player_asd, computer)
        
        score["player"] += result[0]
        score["computer"] += result[1]
        score["draw"] += result[2]
        
        scoreboard(score)
        
if __name__ == "__main__":
    main()