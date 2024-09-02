def main():
    n = 10000
    
    with open('prim.json', 'w') as f:
        f.write('{\n    "data": {\n')
        
        for i in range(2, n + 1):
            for j in range(2, i):
                if i % j == 0:
                    break
            else:
                f.write(f'      "{i}": "prime", \n')
        f.write(f'      "{n}": "prime"' + '\n    }\n}')
                
                

    

if __name__ == '__main__':
    main()