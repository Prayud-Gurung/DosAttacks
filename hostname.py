import socket
from urllib.parse import urlparse

add = "192.1.1.1"
hostname= urlparse(add).hostname

print(hostname)