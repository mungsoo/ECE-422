.section .data
st:
.asciz 	"coolfood"
.global your_asm_fn
.section .text


your_asm_fn:

push	%ebp
mov	%esp,%ebp

#push 	$0x0
#push 	$0x646f6f66
#push 	$0x6c6f6f63
#mov	%esp,%eax
mov	$st,%eax
push 	$0x00c105ed
mov	%esp,%ebx

push 	%eax
push	%ebx
push	$0xacce55ed

call practice
leave
ret
