from Crypto.Cipher import AES
import sys

if len(sys.argv) != 5:
    print("Error: Invalid number of arguments")
    sys.exit()

ciphertext_file = sys.argv[1]
key_file = sys.argv[2]
iv_file = sys.argv[3]
output_file = sys.argv[4]

with open(ciphertext_file) as f:
    ciphertext = f.read().strip()
with open(key_file) as f:
    key = f.read().strip()
with open(iv_file) as f:
    iv = f.read().strip()

obj = AES.new(key.decode("hex"), AES.MODE_CBC, iv.decode("hex"))
text = obj.decrypt(ciphertext.decode("hex"))
print iv
print key
print text

with open(output_file, 'w') as f:
    f.write(text)
    
