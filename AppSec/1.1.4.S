.section .data
st:
.asciz "coolfood"
.global your_asm_fn
.section .text

your_asm_fn:

push	%ebp
mov	%esp,%ebp

mov $st, %eax
push $0xc105ed
mov %esp, %ecx

pushl %eax
pushl %ecx
pushl $0xacce55ed
call practice

leave
ret