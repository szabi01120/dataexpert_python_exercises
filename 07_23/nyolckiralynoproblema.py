def main():
    n = 20
    maradek = n % 12
    paros_list = [i for i in range(2, n + 1, 2)]
    
    if maradek == 3 or maradek == 9:
        paros_list.append(2)
        paros_list.remove(2)
    
    if maradek == 8:
        paratlan_list = [i for i in range(1, n + 1, 2)]
        for i in range(0, len(paratlan_list) - 1, 2):
            paratlan_list[i], paratlan_list[i + 1] = paratlan_list[i + 1], paratlan_list[i]
        paros_list.extend(paratlan_list)
    else:
        paros_list.extend([i for i in range(1, n + 1, 2)])
        
    if maradek == 2:
        a, b = paros_list.index(1), paros_list.index(3)
        paros_list[a], paros_list[b] = paros_list[b], paros_list[a]        
        paros_list.remove(5)
        paros_list.append(5)
        
    if maradek == 3 or maradek == 9:
        paros_list.remove(1)
        paros_list.remove(3)
        paros_list.extend([1, 3])
        
    print(paros_list)
    
if __name__ == '__main__':
    main()