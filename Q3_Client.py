#Client
import socket
import pickle
import threading

HOST = "localhost"  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def send_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        pickled_message = pickle.dumps(message)
        s.sendall(pickled_message)

def receive_messages():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            data = s.recv(1024)
            while data:
                data += s.recv(1024)
            unpickled_data = pickle.loads(data)
            print(unpickled_data)

# Send messages to the server
send_message("Hello, server!")
send_message("How are you?")
send_message("Goodbye!")

# Receive messages from the server
receive_messages()
# Compare this snippet from Q3_Client.py:
