#Real-Time Chat Application with Pickling:

#Develop a simple real-time chat application where multiple clients can communicate with each other via a central server using sockets. 
#Messages sent by clients should be pickled before transmission. The server should receive pickled messages, unpickle them, and broadcast them to all connected clients.


#Requirements:
#Implement separate threads for handling client connections and message broadcasting on the server side.
#Ensure proper synchronization to handle concurrent access to shared resources (e.g., the list of connected clients).
#Allow clients to join and leave the chat room dynamically while maintaining active connections with other clients.
#Use pickling to serialize and deserialize messages exchanged between clients and the server.

#Server
import socket
import threading
import pickle

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on

clients = []  # List to store connected clients

def broadcast_message(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.sendall(message)
            except ConnectionError:
                clients.remove(client)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            # Receive pickled message
            data = conn.recv(1024)
            while data:
                data += conn.recv(1024)
            unpickled_data = pickle.loads(data)

            # Broadcast message to all clients
            broadcast_message(data, conn)
    except (pickle.UnpicklingError, ConnectionError) as e:
        print(f"Error: {e}")
    finally:
        clients.remove(conn)
        conn.close()
        print(f"Disconnected from {addr}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

