import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{timestamp}] {message}")

    with open("client.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

log(f"Connected to {HOST}:{PORT}")

while True:

    command = input("\nEnter command > ")

    if not command:
        continue

    message = "C4P/1.0 " + command

    log(f"SEND > {message}")

    client.sendall(message.encode())

    data = client.recv(1024)

    response = data.decode()

    log(f"RECV > {response}")

    if command == "QUIT":
        break

client.close()

log("Disconnected")