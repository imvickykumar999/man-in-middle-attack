import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect to MITM proxy instead of server directly
client_socket.connect(('127.0.0.1', 9999))

while True:
    message = input("Enter message to send: ")
    client_socket.sendall(message.encode())
    data = client_socket.recv(1024)
    if not data:
        break
    print(f"Received: {data.decode()}")
client_socket.close()

