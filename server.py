import socket
import threading

HOST = "127.0.0.1"
PORT = 12000

def handle_client(conn, addr):
    print("Connected by", addr)

    data = conn.recv(1024)
    if not data:
        conn.close()
        return

    message = data.decode()
    print("Received from", addr, ":", message)

    response = message.upper()
    conn.send(response.encode())

    conn.close()
    print("Connection closed for", addr)


# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print("Server listening on port", PORT)

while True:
    conn, addr = server_socket.accept()

    # Create a new thread for each client
    client_thread = threading.Thread(
        target=handle_client,
        args=(conn, addr)
    )
    client_thread.start()
