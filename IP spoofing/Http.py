import requests

proxies = {
    'http': 'http://user:pass@proxy_ip:port',
    'https': 'http://user:pass@proxy_ip:port'
}

response = requests.get('http://httpbin.org/ip', proxies=proxies)
print(response.text)