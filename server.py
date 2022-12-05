#Server app
import socket
import _thread
import time
import struct
#Currently have it set up to where it starts the race when 3 cars are connected
#This can be changed by changing the car limit variable
car_limit = 3
#Replace with your ip address when you want to test it
address = '129.8.226.210'
counter = 0
def newClient(conn, addr):
    while counter < car_limit:
        time.sleep(0.001)
    conn.send(b"Run")
    while True:
        data = conn.recv(4096)
        if not data:
            break
        print(str(addr)+":"+str(struct.unpack("f",data)))
    conn.close()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((address, 8080))
serv.listen(3)
while True:
    conn, addr = serv.accept()
    print("New Connection!")
    counter += 1
    _thread.start_new_thread(newClient,(conn,addr))