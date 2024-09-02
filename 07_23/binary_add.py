def main():
    a = '1010'
    b = '1011'
    
    print(bin(int(a, 2) + int(b, 2))[2:])
    print(bin(int(a,2)))
    
if __name__ == '__main__':
    main()