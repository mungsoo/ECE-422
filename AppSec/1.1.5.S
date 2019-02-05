.section .data
my_st:
.string		"/bin/sh"
.global _main
.section .text


_main:

push	%ebp
mov	%esp,%ebp
push $0
push $my_st
#eax
mov $11,%eax
#ebx
mov $my_st, %ebx
#ecx
mov %esp, %ecx
lea 4(%esp), %edx

int $0x80

leave
ret

