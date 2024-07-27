import socket
import threading
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

def receive_messages():
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        message = data.decode()
        text_area.insert(tk.END, f"{message}\n\n")

def send_message(event=None):
    message = entry.get()
    entry.delete(0, tk.END)
    text_area.insert(tk.END, f"\t\t\t\t{message}\n\n")
    client_socket.sendall(message.encode())

def start_client():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to MITM proxy instead of server directly
    client_socket.connect(('127.0.0.1', 9999))
    receiver_thread = threading.Thread(target=receive_messages)
    receiver_thread.start()

app = tk.Tk()
app.title("Client Chat")
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

start_client()

app.mainloop()

