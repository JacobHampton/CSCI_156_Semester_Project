#Server app
import socket
import _thread
import time
import struct
# Currently have it set up to where it starts the race when 3 cars are connected
# This can be changed by changing the car limit variable
from threading import Lock
car_limit        = 2
client_limit     = 1
cars             = []
clients          = [] # Array of tuple such that (clientConnection, clientAddress)

#Replace with your ip address when you want to test it
address = '192.168.56.1'

def newCar(carConnection, carAddress, index):
    # When we have no clients connected or our cars is not up to the limit
    while len(clients) < 1 or len(cars) < car_limit:
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
        lastLap = value[0]
        bestLap = min(cars[index])
        averageLap = sum(cars[index]) / len(cars[index])
        result = "Car " + str(index) + ": Last Lap: " + str(round(lastLap, 2)) + ": Best Lap: " + str(round(bestLap,2)) + ", Average Lap: " + str(round(averageLap, 2)) + ", Total time:" + str(round(sum(cars[index]),2))

        # Send all our current data from this car thread to our clients
        for clientConn, clientAddr in clients:
            clientConn.send(result.encode()) 

    carConnection.close()


serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind((address, 8080))
serv.listen(car_limit)

while True:
    connection, address = serv.accept()
    # Connection will respond with its type to determine if it is a car or a client connecting
    type = connection.recv(4096).decode()
    print("Connection from " + str(type) + str(address))

    if type == 'car' and len(cars) < car_limit:
        cars.append([])
        _thread.start_new_thread(newCar,(connection, address, len(cars) - 1))

    elif type == 'client':
        clients.append((connection, address))


serv.close()