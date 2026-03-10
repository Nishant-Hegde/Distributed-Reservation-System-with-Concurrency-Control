import socket
import threading
import json
import os
import logging

HOST = "127.0.0.1"
PORT = 12000

SEAT_FILE = "seats.json"

# Lock for concurrency control
lock = threading.Lock()

# Logging configuration
logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Load seat data from file
def load_seats():
    if os.path.exists(SEAT_FILE):
        with open(SEAT_FILE, "r") as f:
            return json.load(f)
    else:
        seats = {str(i): False for i in range(1, 6)}
        save_seats(seats)
        return seats


# Save seat data to file
def save_seats(seats):
    with open(SEAT_FILE, "w") as f:
        json.dump(seats, f)


seats = load_seats()


def handle_client(conn, addr):
    try:
        data = conn.recv(1024)
        if not data:
            return

        message = data.decode().strip()
        print("Request from", addr, ":", message)
        logging.info(f"{addr} -> {message}")

        # STATUS command
        if message == "STATUS":
            with lock:
                status = ""
                for seat in seats:
                    if seats[seat]:
                        status += f"{seat}:BOOKED "
                    else:
                        status += f"{seat}:FREE "

            conn.send(status.encode())
            return

        parts = message.split()

        if len(parts) != 2 or parts[0] != "RESERVE":
            conn.send("INVALID_COMMAND".encode())
            return

        seat_id = parts[1]

        if not seat_id.isdigit():
            conn.send("INVALID_SEAT_NUMBER".encode())
            return

        with lock:

            if seat_id not in seats:
                response = "FAILED_INVALID_SEAT"

            elif seats[seat_id]:
                response = "FAILED_ALREADY_BOOKED"

            else:
                seats[seat_id] = True
                save_seats(seats)
                response = "SUCCESS"

        conn.send(response.encode())
        logging.info(f"{addr} <- {response}")

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