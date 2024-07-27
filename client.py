# client.py
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to MITM proxy instead of server directly
client_socket.connect(('127.0.0.1', 9999))
client_socket.sendall(b"Hello from client")
data = client_socket.recv(1024)
print(f"Received: {data.decode()}")
client_socket.close()

