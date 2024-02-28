#Implement a client-server file transfer application where the client sends a file to the server using sockets. 
#Before transmitting the file, pickle the file object on the client side. On the server side, receive the pickled file object, unpickle it, and save it to disk.


#Requirements:
#The client should provide the file path of the file to be transferred.
#The server should specify the directory where the received file will be saved.
#Ensure error handling for file I/O operations, socket connections, and pickling/unpickling.

#Server
import socket
import pickle
import os

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on
SAVE_DIR = "received_files"  # Directory to save received files

def save_file(data, filename):
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)  # Create directory if it doesn't exist
        with open(os.path.join(SAVE_DIR, filename), "wb") as f:
            f.write(data)
        print(f"File '{filename}' saved successfully.")
    except OSError as e:
        print(f"Error saving file: {e}")

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        # Receive pickled file object
        data = conn.recv(1024)
        while data:
            data += conn.recv(1024)
        unpickled_data = pickle.loads(data)

        # Extract filename and file data
        filename, file_data = unpickled_data

        # Save the received file
        save_file(file_data, filename)
    except (pickle.UnpicklingError, ConnectionError, OSError) as e:
        print(f"Error: {e}")
    finally:
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        handle_client(conn, addr)

#Client
def send_file(filepath):
    try:
        with open(filepath, "rb") as f:
            file_data = f.read()
            filename = os.path.basename(filepath)

            # Pickle the filename and file data
            data = pickle.dumps((filename, file_data))

            # Connect to the server and send pickled data
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(data)
            print(f"File '{filename}' sent successfully.")
    except (FileNotFoundError, PermissionError, ConnectionError, pickle.PicklingError) as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    filepath = input("Enter the file path: ")
    send_file(filepath)
