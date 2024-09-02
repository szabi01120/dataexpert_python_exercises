import random

def comp_choice(szotar):
    return random.randint(0, len(szotar) - 1)

def main():
    szotar = ["anya", "apa", "szótár", "valami"]
    valasztott_szo = szotar[comp_choice(szotar)]
    valasztott_secret = ["_"] * len(valasztott_szo)
    print(valasztott_secret)
    
    while '_' in valasztott_secret:
        try:
            betu = input("Adj meg egy betűt: ")
            if len(betu) != 1:
                raise ValueError
        except ValueError:
            print("Csak egy betűt adj meg!")
            continue
        hossz = len(valasztott_szo)
        
        if betu in valasztott_szo:
            for i, char in enumerate(valasztott_szo):
                if char == betu:
                    valasztott_secret[i] = betu
            print(valasztott_secret)
        else:
            print("Ez sajnos nem talált!")
    
    
if __name__ == "__main__":
    main()