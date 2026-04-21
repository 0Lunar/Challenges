from scapy.all import *
import json


if __name__ == "__main__":
    pcap = PcapReader("traffic.pcap")
    packets = []
    auth_codes = {}
    
    for packet in pcap:
        if packet.haslayer(TCP):
            packet = bytes(packet[TCP].payload)
            
            if packet:
                packets.append(packet.strip())
    
    
    for pk in range(len(packets) - 2):
        if packets[pk].isdigit() and packets[pk + 1].isdigit() and packets[pk + 2].startswith(b'1. Login con password'):
            auth_codes[int(packets[pk].decode())] = int(packets[pk + 1].decode())
    
    with open("codes.json", "wt") as f:
        json.dump(auth_codes, f)