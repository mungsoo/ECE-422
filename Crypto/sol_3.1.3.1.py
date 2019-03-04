#python sol_3.1.3.1.py 3.1.3.1_input_string.txt 3.1.3.1_perturbed_string.txt sol_3.1.3.1.hex
import sys
from Crypto.Hash import SHA256

if len(sys.argv) != 4:
    print("Error: Invalid number of arguments")
    sys.exit()

file1 = sys.argv[1]
file2 = sys.argv[2]
output_file = sys.argv[3]

with open(file1) as f:
    string1 = f.read().strip()
with open(file2) as f:
    string2 = f.read().strip()

h = SHA256.new()
sha1 = h.update(string1)
sha1 = h.hexdigest()
h = SHA256.new()
sha2 = h.update(string2)
sha2 = h.hexdigest()
print sha1
print sha2
bin1 = bin(int(sha1, 16))[2:]
bin2 = bin(int(sha2, 16))[2:]
length = max(len(bin1),len(bin2))
bin1 = bin1.zfill(length)
bin2 = bin2.zfill(length)

hamming_dist = 0
for idx in range(length):
	if bin1[idx] != bin2[idx]:
		hamming_dist += 1
text = hex(hamming_dist)[2:]
print text

with open(output_file, 'w') as f:
    f.write(text)