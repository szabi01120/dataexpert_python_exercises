s = "babad"
result = ""
charset = set()
left = 0
max_len = 0

for i in range(len(s)):
    if s[i] not in charset:
        charset.add(s[i])
        max_len = max(max_len, i - left + 1)
    else:
        while s[i] in charset:
            charset.remove(s[left])
            left += 1
        charset.add(s[i])    

print(charset)
        