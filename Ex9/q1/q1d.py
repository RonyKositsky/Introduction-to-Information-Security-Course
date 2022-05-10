from scapy.all import *


def on_packet(packet):
    """Implement this to send a SYN ACK packet for every SYN.

    Notes:
    1. Use *ONLY* the `send` function from scapy to send the packet!
    """
    if not packet.haslayer(TCP):
        return
    
    if not packet.getlayer(TCP).flags == 2: #syn
        return
    
    ip_layer = packet.getlayer(IP)
    tcp_layer = packet.getlayer(TCP)
    
    ip = IP(dst = ip_layer.src, src = ip_layer.dst)
    tcp = TCP(dport = tcp_layer.sport, sport = tcp_layer.dport, flags = 'SA', ack = tcp_layer.seq + 1)

    send(ip/tcp) 


def main(argv):
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    sniff(prn=on_packet)


if __name__ == '__main__':
    # WARNING: DO NOT MODIFY THIS FUNCTION!
    import sys
    sys.exit(main(sys.argv))
