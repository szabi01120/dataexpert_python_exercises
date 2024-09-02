import random

def main():
    try:
        with open("excuses.txt", "r") as file:
            excuses = file.readlines()
    except FileNotFoundError:
        print("Nincs ilyen fájl!")
        return
    print(random.choice(excuses))
        
    
if __name__ == '__main__':
    main()