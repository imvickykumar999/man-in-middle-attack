import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

def handle_client(client_socket, text_area):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode()
        text_area.insert(tk.END, f"{message}\n\n")
    client_socket.close()

def send_message(event=None):
    message = entry.get()
    entry.delete(0, tk.END)
    text_area.insert(tk.END, f"\t\t\t\t{message}\n\n")
    client_socket.sendall(message.encode())

def start_server():
    global client_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(1)
    #text_area.insert(tk.END, "Server listening on port 12345\n")
    client_socket, addr = server_socket.accept()
    #text_area.insert(tk.END, f"Connection from {addr}\n")
    client_thread = threading.Thread(target=handle_client, args=(client_socket, text_area))
    client_thread.start()

app = tk.Tk()
app.title("Server Chat")
app.geometry("400x800")

text_area = ScrolledText(app, wrap=tk.WORD)
text_area.pack(expand=True, fill=tk.BOTH)

entry_frame = tk.Frame(app)
entry_frame.pack(fill=tk.X)

entry = tk.Entry(entry_frame)
entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
entry.bind("<Return>", send_message)

send_button = tk.Button(entry_frame, text="Send", command=send_message)
send_button.pack(side=tk.RIGHT)

start_server()

app.mainloop()

