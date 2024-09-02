words = ["abc","bcd","aaaa","cbc"]
x = 'a'
rlist = []

rlist = []
for i in range(len(words)):
    if words[i].find(x) != -1:
        rlist.append(i)
print(rlist)