import time
import os
from scapy.all import *


WINDOW = 60
MAX_ATTEMPTS = 15


# Initialize your data structures here
log = dict()
blocked = set()  # We keep blocked IPs in this set
syn_packets_log = dict()


def on_packet(packet):
    """This function will be called for each packet.

    Use this function to analyze how many packets were sent from the sender
    during the last window, and if needed, call the 'block(ip)' function to
    block the sender.

    Notes:
    1. You must call block(ip) to do the blocking.
    2. The number of SYN packets is checked in a sliding window.
    3. Your implementation should be able to efficiently handle multiple IPs.
    """
       
    if not packet.haslayer(TCP):
        return
    
    if not packet.getlayer(TCP).flags == 2: #syn
        return
        
    ip = packet.getlayer(IP).src
    if ip in blocked:
        return
        
    time = packet.time
    if ip in log:
        if len(log[ip]) == MAX_ATTEMPTS:
            block(ip)
        
        else:
            log[ip].sort()
            log[ip].append(time)
            if log[ip][0] < (time - WINDOW):   # Check the window.           
                log[ip] = log[ip].pop(0) 
       
    else:
        log[ip] = [time]


def generate_block_command(ip: str) -> str:
    """Generate a command that when executed in the shell, blocks this IP.

    The blocking will be based on `iptables` and must drop all incoming traffic
    from the specified IP."""
    return f"sudo iptables -A INPUT -s {ip} -j DROP"


def block(ip):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    os.system(generate_block_command(ip))
    blocked.add(ip)


def is_blocked(ip):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    return ip in blocked


def main():
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(prn=on_packet)


if __name__ == '__main__':
    main()
