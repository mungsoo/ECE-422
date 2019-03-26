from scapy.all import *

import sys

def debug(s):
    print('#{0}'.format(s))
    sys.stdout.flush()

if __name__ == "__main__":
    conf.iface = sys.argv[1]
    ip_addr = sys.argv[2]

    # SYN scan
    src_ip = "10.4.22.176"
    dst_ip = ip_addr
    sport = 12345
    
    print("#Start scanning on %s..." % dst_ip)
    for dport in range(1, 1025):
        resp = sr1(IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags="S"), \
verbose=0, iface=conf.iface, timeout=5)

        if resp and resp.haslayer(TCP) and resp.getlayer(TCP).flags == 0x12:
                print("<%s,%d>" % (dst_ip, dport))
                sr1(IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport, flags="R"), \
verbose=0, iface=conf.iface, timeout=5)
    print("#End scanning...")


