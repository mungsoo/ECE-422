#python yifan_3.1.2.3.py 3.1.2.3_aes_weak_ciphertext.hex
from Crypto.Cipher import AES
import sys

if len(sys.argv) != 2:
    print("Error: Invalid number of arguments")
    sys.exit()

ciphertext_file = sys.argv[1]
#output_file = sys.argv[2]

with open(ciphertext_file) as f:
    ciphertext = f.read().strip()
# with open(key_file) as f:
#     key = f.read().strip()
# with open(iv_file) as f:
#     iv = f.read().strip()
iv = '0'*32 # 128
for i in range(2**5):
	# i from 0 to 31
	key = '00'*31 + format(i, '02x')
	print(key)
	obj = AES.new(key.decode("hex"), AES.MODE_CBC, iv.decode("hex"))
	text = obj.decrypt(ciphertext.decode("hex"))
	#print key
	# with open(output_file, 'w') as f:
	#     f.write(text)
	print text+'\n'

# key = '000000000000000000000000000000000000000000000000000000000000001d'
# obj = AES.new(key.decode("hex"), AES.MODE_CBC, iv.decode("hex"))
# text = obj.decrypt(ciphertext.decode("hex"))
# print text