import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(1)
print("Server listening on port 12345")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode()}")
        response = f"Server received: {data.decode()}"
        client_socket.sendall(response.encode())
    client_socket.close()

