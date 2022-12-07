# Import the necessary modules
import threading
import tkinter as tk
from tkinter import font
import socket

# Replace with your ip address when you want to test it
address = '192.168.1.245'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, 8080))
client.send(b'client')

# Create a Tkinter window
root = tk.Tk()
my_font = font.Font(family='Helvetica', size=20)
my_header_font = font.Font(family='Helvetica', size=20, weight='bold')
# Add a label to the window
title = tk.Label(root, text='Times:', font=my_header_font)
label = tk.Label(root, text='Waiting for data...', font=my_font)
title.pack()
label.pack()

# Create a function that will be called when data is received
def update_label(data):
  # Update the text of the label
  if label['text'] == 'Waiting for data...':
    label['text'] =  data + '\n'
  else:
    label['text'] =  label['text'] + data + '\n'

# Create a function that will run in a separate thread and handle the socket
# communication
def socket_thread():
  # Set up a loop that will receive data from the server and call the update_label
  # function when new data is received
  while True:
    from_server = client.recv(4096)
    # Update the label with the received data
    update_label(from_server.decode())

# Create a new thread for the socket communication
thread = threading.Thread(target=socket_thread)

# Start the thread
thread.start()

# Start the Tkinter event loop
root.mainloop()