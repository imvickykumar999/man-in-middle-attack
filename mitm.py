# mitm.py
import socket
import threading

def handle_client(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    while True:
        # Receive data from the client
        local_data = client_socket.recv(4096)
        if len(local_data):
            print(f"Intercepted from client: {local_data.decode()}")
            # Send the received data to the remote host
            remote_socket.send(local_data)

        # Receive data from the remote host
        remote_data = remote_socket.recv(4096)
        if len(remote_data):
            print(f"Intercepted from server: {remote_data.decode()}")
            # Send the received data to the client
            client_socket.send(remote_data)

    client_socket.close()
    remote_socket.close()

def start_mitm(local_host, local_port, remote_host, remote_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((local_host, local_port))
    server.listen(5)
    print(f"[*] Listening on {local_host}:{local_port}")

    while True:
        client_socket, addr = server.accept()
        print(f"[*] Accepted connection from {addr}")

        proxy_thread = threading.Thread(
            target=handle_client, args=(client_socket, remote_host, remote_port)
        )
        proxy_thread.start()

if __name__ == "__main__":
    local_host = '0.0.0.0'
    local_port = 9999
    remote_host = '127.0.0.1'
    remote_port = 12345

    start_mitm(local_host, local_port, remote_host, remote_port)

