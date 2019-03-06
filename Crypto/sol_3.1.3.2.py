import sys

if len(sys.argv) != 3:
    print("Error: Invalid number of arguments")
    sys.exit()

input_file = sys.argv[1]
output_file = sys.argv[2]


def WHA(in_str):
    out_hash = 0
    mask = 0x3FFFFFFF

    for byte in in_str:
        byte = ord(byte)
        intermediate_value = ((byte ^ 0xCC) << 24) | \
                             ((byte ^ 0x33) << 16) | \
                             ((byte ^ 0xAA) << 8)  | \
                             (byte ^ 0x55)
        out_hash = (out_hash & mask) + (intermediate_value & mask)
        
    
    return hex(out_hash)


with open(input_file) as f:
   in_str = f.read().strip()

# instr="THE PEOPLE IN 1917 OF THIS US COMMONWEALTH IN THE CARIBBEAN BECAME NATURALIZED CITIZENS"
out_hash = WHA(in_str)

with open(output_file, "w") as f:
    f.write(out_hash[2:10])