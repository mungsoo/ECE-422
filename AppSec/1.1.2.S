.global your_asm_fn
.section .text

your_asm_fn:

push	%ebp
mov	%esp,%ebp
pushl $0xc001f00d
pushl $0xc105ed
pushl $0xacce55ed
call practice
#add $12, %esp

leave
ret