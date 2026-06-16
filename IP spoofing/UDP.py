from scapy.all import IP, UDP, send
from faker import Faker

fake = Faker()
source = fake.ipv4()
destination = fake.ipv4()
ip = IP(src=source, dst=destination)

udp = UDP(sport=3355, dport=3355)
data = b"Hello"

pkt = ip/udp/data
pkt.show()
# print(pkt.summary())

send(pkt, verbose=0)