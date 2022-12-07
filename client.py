# Import the necessary modules
import threading
import tkinter as tk
import socket

# Replace with your ip address when you want to test it
address = '192.168.1.245'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, 8080))
client.send(b'client')

# Create a Tkinter window
root = tk.Tk()

# Add a label to the window
label = tk.Label(root, text='Waiting for data...')
label.pack()

# Create a function that will be called when data is received
def update_label(data):
  # Update the text of the label
  label['text'] = data

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