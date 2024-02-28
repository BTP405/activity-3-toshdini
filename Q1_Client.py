#Q1- Client
import socket
import pickle
import os

HOST = "localhost"  # The server's hostname or IP address
PORT = 65432        # The port used by the server

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
