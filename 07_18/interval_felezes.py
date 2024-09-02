# guess the number intervallum felezéssel
import random

def main():
    min_num = int(input("Add meg a minimum számot: "))
    max_num = int(input("Add meg a maximum számot: "))

    print("Gondolj egy számra...")

    flag = False

    while not flag:
        guess = (min_num + max_num) // 2
        print(guess, " volt a gondolt szám?")
        
        answer = input()
        if answer.lower() == "igen":
            print("Kitaláltam a számot")
            flag = True
            
        if answer.lower() == "nem":
            print("Kisebb vagy nagyobb a szám? (+ / -)")
            answer = input()          
            if answer == "-":
                max_num = guess - 1
            elif answer == "+":
                min_num = guess + 1
    
if __name__ == "__main__":
    main()    