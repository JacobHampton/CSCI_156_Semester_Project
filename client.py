import threading
import tkinter as tk
from tkinter import font
import socket

# Replace with your ip address when you want to test it
address = '192.168.1.245'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((address, 8080))
client.send(b'client')
total_times = 0

window = tk.Tk()
window.title("TCP Client") 
running_font = font.Font(family='Helvetica', size=20)
header_font = font.Font(family='Helvetica', size=20, weight='bold')
# Add the text to the window (for some reason tkinter calls the text labels)
title = tk.Label(window, text='0 Total Times Recorded:', font=header_font)
messages = tk.Label(window, text='Waiting for data...', font=running_font)
title.pack()
messages.pack()

# Create a function that will be called when data is received
def update_label(data):
  # Update the text of the label
  if messages['text'] == 'Waiting for data...':
    messages['text'] =  data + '\n'
  else:
    messages['text'] =  messages['text'] + data + '\n'
  title['text'] = str(total_times) + " Total Times Recorded:"

# Create a function that will run in a separate thread and handle the socket while loop / recieving
def newSocket():
  global total_times
  while True:
    from_server = client.recv(4096)
    # Update the label with the received data
    total_times += 1
    update_label(from_server.decode())

# Create a new thread for the socket communication
thread = threading.Thread(target=newSocket)

thread.start()
window.mainloop()