import socket
import threading

def handle_client(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    def forward_data(source, destination, direction):
        while True:
            data = source.recv(4096)
            if not data:
                break
            if direction == "client_to_server":
                print(f"Intercepted from client: {data.decode()}")
                # Optionally modify data here
                data += b" : altered"
            elif direction == "server_to_client":
                print(f"Intercepted from server: {data.decode()}")
                # Optionally modify data here
            destination.send(data)
    
    client_thread = threading.Thread(target=forward_data, args=(client_socket, remote_socket, "client_to_server"))
    server_thread = threading.Thread(target=forward_data, args=(remote_socket, client_socket, "server_to_client"))

    client_thread.start()
    server_thread.start()

    client_thread.join()
    server_thread.join()
    
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

