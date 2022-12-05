#Cars with transponders
import socket
import time
import random
import struct

#Replace with your ip address when you want to test it
address = '129.8.226.210'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, 8080))
flag = True
while flag:
    from_server = client.recv(4096)
    if from_server == b"Run":
        flag = False
for i in range(5):
    random1 = round(random.uniform(13.00,16.00),2)
    time.sleep(random1)
    client.send(bytearray(struct.pack("f",random1)))
client.close()