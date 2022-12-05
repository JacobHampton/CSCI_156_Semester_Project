#Server app
import socket
import _thread
import time
import struct
#Currently have it set up to where it starts the race when 3 cars are connected
#This can be changed by changing the car limit variable
from threading import Lock
car_limit = 3
#Replace with your ip address when you want to test it
address = '129.8.226.210'

counter = 0
cars = []
def newCar(conn, addr, index):
    while counter < car_limit:
        time.sleep(0.0001)
    conn.send(b"Run")
    while True:
        data = conn.recv(4096)
        if not data:
            break
        value = struct.unpack("f",data)
        cars[index].append(value[0])
        bestLap = min(cars[index])
        averageLap = sum(cars[index])/len(cars[index])
        print(str(index)+": Best Lap: "+str(bestLap)+", Average Lap: " +str(averageLap)+", Total time:"+str(sum(cars[index])))
    conn.close()

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((address, 8080))
serv.listen(3)
flag = True
while flag:
    conn, addr = serv.accept()
    print("New Connection!")
    cars.append([])
    counter += 1
    _thread.start_new_thread(newCar,(conn,addr, counter-1))
serv.close()