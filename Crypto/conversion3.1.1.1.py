# 3.1.1.1
with open('3.1.1.2_value.hex') as f:
    file_content = f.read().strip()

print(file_content)
# parse the string into a binary array representing the hexadecimal number
# binary_content = file_content.decode('hex')
# print(binary_content)
#import binascii
#print(binascii.hexlify(file_content))

# parse the string into integer
integer_parsed = int(file_content,16)
print(integer_parsed)

#hex 
hex_parsed = hex(integer_parsed)
print(hex_parsed)


# Binary
binary_parsed = bin(integer_parsed)[2:]
print(str(binary_parsed))