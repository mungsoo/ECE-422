# with open("3.1.1.2_value.hex") as f:
#     file_content = f.read().strip()
# integer_parsed = int(file_content, 16)
# print(bin(integer_parsed)[2:])
from Crypto.Cipher import AES
import sys

if len(sys.argv) != 2:
    print("Error: Invalid number of arguments")
    sys.exit()

ciphertext_file = sys.argv[1]
#output_file = sys.argv[2]

with open(ciphertext_file) as f:
    ciphertext = f.read().strip()
    
iv = "0" * 32
for i in range(32):
    key = "0" * 62
    if i >= 16:
        key += ('1' + hex(i-16)[2:])
    else:
        key += ('0' + hex(i)[2:])
    obj = AES.new(key.decode("hex"), AES.MODE_CBC, iv.decode("hex"))
    text = obj.decrypt(ciphertext.decode("hex"))
    print("%d\n\n" % i)
    print("%d : %s\n" % (i, text))
    