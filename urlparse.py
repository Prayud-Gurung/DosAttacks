from urllib.parse import urlparse
import socket

address = "https://salma-southmost-archimedes.ngrok-free.dev/login"
hostname = urlparse(address)
print(hostname.netloc)
print(hostname.hostname)
ip = socket.gethostbyname(hostname.hostname)
print(ip)