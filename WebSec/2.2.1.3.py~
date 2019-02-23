from hashlib import md5
import os
target = b"'or'"

for i in range(14373608294, 999999999999999):
    bts = str(i).encode()
    hash = md5(bts).digest()
    if target in hash and 49<=hash[hash.index(b"'or'") + 4]<=57:
        print("Here you go!:", bts)
        break
    elif i % 10000 == 0:
        print("Hash :", bts)
        print("target :", target)
