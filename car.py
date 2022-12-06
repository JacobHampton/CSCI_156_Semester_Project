#Cars with transponders
import socket
import time
import random
import struct

#Replace with your ip address when you want to test it
address = '192.168.56.1'
lap_count = 2
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, 8080))
client.send(b'car')
# Wait until we receive from the server that we are registered.
flag = True
while flag:
    from_server = client.recv(4096)
    if from_server == b"Run":
        flag = False

# Send the random time data
for i in range(lap_count):
    random1 = round(random.uniform(13.00,16.00),2)
    time.sleep(random1)
    client.send(bytearray(struct.pack("f",random1)))

client.close()