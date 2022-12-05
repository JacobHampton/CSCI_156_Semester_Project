#Server app
import socket
import _thread
import time
import struct
# Currently have it set up to where it starts the race when 3 cars are connected
# This can be changed by changing the car limit variable
from threading import Lock
car_limit        = 3
client_limit     = 3
cars             = []
clients          = [] # Array of tuple such that (clientConnection, clientAddress)

#Replace with your ip address when you want to test it
address = '129.8.238.43'

def newCar(carConnection, carAddress, index):
    # When we don't have enough cars wait until they're all connected
    while len(clients) < client_limit:
        time.sleep(0.0001)
    # To the carConnection send a 'signal' for it to run.
    carConnection.send(b"Run")
    # Wait to receive data back from our car and print and store it
    while True:
        data = carConnection.recv(4096)

        if not data:
            break

        value = struct.unpack("f",data)
        cars[index].append(value[0])
        bestLap = min(cars[index])
        averageLap = sum(cars[index]) / len(cars[index])
        result = str(index) + ": Best Lap: " + str(bestLap) + ", Average Lap: " + str(averageLap) + ", Total time:" + str(sum(cars[index]))

        # Send all our current data from this car thread to our clients
        for clientConn, clientAddr in clients:
            clientConn.send(result.encode()) 

    carConnection.close()


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((address, 8080))
# Listen for the three cars?
# serv.listen(3)
serv.listen(car_limit)

flag = True
while flag:
    connection, address = serv.accept()
    # Start with car connections then client connections
    if len(cars) < car_limit:
        cars.append([])
        _thread.start_new_thread(newCar,(connection, address, len(cars) - 1))
    else:
        clients.append((connection, address))


serv.close()