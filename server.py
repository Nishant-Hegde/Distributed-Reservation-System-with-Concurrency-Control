import socket

HOST = "127.0.0.1"   # localhost
PORT = 12000

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind and listen
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Server is listening on port", PORT)

while True:
    # Accept a client
    conn, addr = server_socket.accept()
    print("Connected by", addr)

    # Receive data
    data = conn.recv(1024)
    if not data:
        conn.close()
        continue

    message = data.decode()
    print("Received:", message)

    # Send response
    response = message.upper()
    conn.send(response.encode())

    # Close client connection
    conn.close()
