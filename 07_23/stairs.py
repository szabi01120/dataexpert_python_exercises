def main():
    n = 5
    if n == 1:
        return print(1)
    elif n == 2:
        return print(2)

    a,b,c = 0,1,0
    
    for i in range(n):
        c = a + b
        a,b = b,c
    return print(b)    
    
    
    
if __name__ == '__main__':
    main()