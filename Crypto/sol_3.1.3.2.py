#WHA
#
import sys
import random
import string

if len(sys.argv) != 3:
    print("Error: Invalid number of arguments")
    sys.exit()
input_file= sys.argv[1]
output_file= sys.argv[2]

with open(input_file) as f:
    input_str = f.read().strip()
#input_str = "IGroot.  am"
hex_str = input_str.encode("hex")
print hex_str
Mask = 0x3FFFFFFF
outHash = 0
for i in range(len(input_str)):
	# byte = input_str[i].encode('hex')
	# integer_parsed = int(byte,16)
	byte = ord(input_str[i])
	intermediate_value = ((byte ^ 0xCC) << 24) | ((byte ^ 0x33) << 16) | ((byte ^ 0xAA) << 8) | (byte ^ 0x55)
	outHash = (outHash & Mask) + (intermediate_value & Mask)
#print outHash
print hex(outHash)

with open(output_file, 'w') as f:
    f.write(hex(outHash)[2:])

