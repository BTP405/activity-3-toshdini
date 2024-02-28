#Distributed Task Queue with Pickling:

#Create a distributed task queue system where tasks are sent from a client to multiple worker nodes for processing using sockets. 
#Tasks can be any Python function that can be pickled. Implement both the client and worker nodes. 
#The client sends tasks (pickled Python functions and their arguments) to available worker nodes, and each worker node executes the task and returns the result to the client.

#Requirements:
#Implement a protocol for serializing and deserializing tasks using pickling.
#Handle task distribution, execution, and result retrieval in both the client and worker nodes.
#Ensure fault tolerance and scalability by handling connection errors, timeouts, and dynamic addition/removal of worker nodes.

#Client 
import socket
import pickle
import os
import time

HOST = "localhost"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to connect to
WORKER_NODES = [("localhost", 65433), ("localhost", 65434)]  # List of worker nodes

def send_task(func, args, worker_nodes):
    for worker in worker_nodes:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(worker)
                pickled_task = pickle.dumps((func, args))
                s.sendall(pickled_task)
                print(f"Task sent to {worker}")
            except (ConnectionError, OSError) as e:
                print(f"Error: {e}")

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y if y != 0 else "Error: Division by zero"

# Send tasks to worker nodes
send_task(add, (5, 3), WORKER_NODES)
send_task(subtract, (10, 7), WORKER_NODES)
send_task(multiply, (2, 4), WORKER_NODES)
send_task(divide, (9, 0), WORKER_NODES)
send_task(divide, (9, 3), WORKER_NODES)

#Worker
def handle_task(conn):
    try:
        # Receive pickled task
        data = conn.recv(1024)
        while data:
            data += conn.recv(1024)
        unpickled_data = pickle.loads(data)

        # Extract function and arguments
        func, args = unpickled_data

        # Execute the task
        result = func(*args)

        # Send the result back to the client
        pickled_result = pickle.dumps(result)
        conn.sendall(pickled_result)
    except (pickle.UnpicklingError, ConnectionError, OSError) as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def start_worker(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Worker node running on {host}:{port}")
        while True:
            conn, addr = s.accept()
            handle_task(conn)

# Start worker nodes
for i, worker in enumerate(WORKER_NODES):
    host, port = worker
    start_worker(host, port)