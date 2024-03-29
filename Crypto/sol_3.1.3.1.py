import math
import sys
from hashlib import sha256
if len(sys.argv) != 4:
    print("Error: Invalid number of arguments")
    sys.exit()

file_1 = sys.argv[1]
file_2 = sys.argv[2]
output_file = sys.argv[3]

with open(file_1) as f:
    text_1 = f.read().strip()
with open(file_2) as f:
    text_2 = f.read().strip()

hash_1 = int(sha256(text_1).hexdigest(), 16)
hash_2 = int(sha256(text_2).hexdigest(), 16)

distance = bin((hash_1 ^ hash_2)).count("1")

with open(output_file, "w") as f:
    f.write(hex(distance)[2:])

