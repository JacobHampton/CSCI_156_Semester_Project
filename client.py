# Clients / Runners
import socket

# Replace with your ip address when you want to test it
address = '192.168.1.245'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, 8080))
client.send(b'client')
flag = True
while flag:
    from_server = client.recv(4096)
    print(from_server.decode());
    
client.close()