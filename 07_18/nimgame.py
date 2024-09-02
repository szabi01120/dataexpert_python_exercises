def my_turn():
    while True:
        try:
            take = int(input("Hány golyót veszel el az asztalró? (1, 2, 3): "))
            if take in [1,2,3]:
                return take
            else: 
                print("Az alábbi számok közüls válassz: (1, 2, 3)")
        except ValueError:
            print("Az alábbi számok közül válassz: (1, 2, 3)")
            continue

def computer_turn(golyo):
    take = (golyo - 1) % 4
    if take == 0:
        take = 1
    print(f"A gép {take} golyót vesz el.")
    return take

def main():
    golyo = 21
    print(f"{golyo} golyó van az asztalon")
    
    while golyo > 0:
        # mi választunk
        my_take = my_turn()
        print(golyo)
        golyo -= my_take
        print(f"{golyo} golyó maradt az asztalon")
        
        if golyo == 0:
            print("Te vetted el az utolsó golyót. Sajnos vesztettél")
            break
        
        # gép választ
        computer_take = computer_turn(golyo)
        golyo -= computer_take
        print(f"{golyo} golyó maradt az asztalon")
        
        if golyo == 0:
            print("A gép vette el az utolsó golyót, te nyertél!")
            break
    
if __name__ == "__main__":
    main()