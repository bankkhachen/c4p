import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5000


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{timestamp}] {message}")

    with open("server.log", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")


def process_message(message):
    parts = message.strip().split(" ", 2)

    if len(parts) < 2:
        return "C4P/1.0 400 BAD_REQUEST Invalid message"

    version = parts[0]
    command = parts[1]

    if version != "C4P/1.0":
        return "C4P/1.0 400 BAD_REQUEST Unsupported protocol version"

    if command == "JOIN":
        if len(parts) < 3:
            return "C4P/1.0 400 BAD_REQUEST Missing player name"

        name = parts[2]

        return f"C4P/1.0 201 JOINED Welcome {name}"

    elif command == "MOVE":
        if len(parts) < 3:
            return "C4P/1.0 400 BAD_REQUEST Missing column"

        try:
            column = int(parts[2])

            if column < 1 or column > 7:
                return "C4P/1.0 400 BAD_REQUEST Invalid column"

        except ValueError:
            return "C4P/1.0 400 BAD_REQUEST Column must be a number"

        return f"C4P/1.0 200 OK Move accepted column={column}"

    elif command == "STATUS":
        return "C4P/1.0 200 OK Game is waiting"

    elif command == "QUIT":
        return "C4P/1.0 221 BYE Goodbye"

    else:
        return "C4P/1.0 400 BAD_REQUEST Unknown command"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(1)

log(f"Server started on {HOST}:{PORT}")
log("Waiting for client...")

conn, addr = server.accept()

log(f"Client connected: {addr}")

while True:

    data = conn.recv(1024)

    if not data:
        break

    message = data.decode().strip()

    log(f"RECV > {message}")

    response = process_message(message)

    log(f"SEND > {response}")

    conn.sendall(response.encode())

    if message.endswith("QUIT"):
        break

conn.close()
server.close()

log("Server stopped")