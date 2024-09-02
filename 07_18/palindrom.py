def main():
    szoveg = input("Add meg a szöveget: ")
    if szoveg.replace(" ", "") == szoveg[::-1].replace(" ", ""):
        print("palindrom")
    else:
        print("nem palindrom")
    
if __name__ == "__main__":
    main()