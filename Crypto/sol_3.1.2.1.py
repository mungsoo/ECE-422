import sys

if len(sys.argv) != 4:
    print("Error: Invalid number of arguments")
    sys.exit()
ciphertext_file, key_file, output_file = sys.argv[1], sys.argv[2], sys.argv[3]

with open(ciphertext_file) as f:
    ciphertext = f.read().strip()
with open(key_file) as f:
    key = f.read().strip()
    
# print(ciphertext)
# print(key)
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

result = []
for i, v in enumerate(ciphertext):
    if v.isalpha():
        #result.append(key[ord(v) - ord('A')])
        index = key.find(v)
        result.append(alpha[index])
    else:
        result.append(v)

with open(output_file, 'w') as f:
    f.write("".join(result))
# print("".join(result))