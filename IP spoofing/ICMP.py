from scapy.all import IP, ICMP, sr
from faker import Faker

fake = Faker()

sourceIP = fake.ipv4()
destinationIP = fake.ipv4()

packet = IP(src = sourceIP, dst = destinationIP)/ ICMP()
packet.show()
print(packet.summary())

answered, unanswered = sr(packet, verbose=0, timeout=5)
print(answered)
