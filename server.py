import socket
import threading

HOST = "127.0.0.1"
PORT = 12000

# Shared resource: seats
seats = {
    1: False,
    2: False,
    3: False,
    4: False,
    5: False
}

# Lock for concurrency control
lock = threading.Lock()


def handle_client(conn, addr):
    try:
        data = conn.recv(1024)
        if not data:
            return

        message = data.decode().strip()
        print("Request from", addr, ":", message)

        parts = message.split()

        if len(parts) != 2 or parts[0] != "RESERVE":
            conn.send("INVALID_COMMAND".encode())
            return

        seat_id = int(parts[1])

        # ----- CRITICAL SECTION -----
        with lock:
            if seat_id not in seats:
                response = "FAILED_INVALID_SEAT"
            elif seats[seat_id]:
                response = "FAILED_ALREADY_BOOKED"
            else:
                seats[seat_id] = True
                response = "SUCCESS"
        # ----- END CRITICAL SECTION -----

        conn.send(response.encode())

    finally:
        conn.close()


# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print("Reservation server running on port", PORT)

while True:
    conn, addr = server_socket.accept()
    threading.Thread(
        target=handle_client,
        args=(conn, addr)
    ).start()
