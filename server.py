import socket
import threading
import json
import os
import logging
import ssl

HOST = "127.0.0.1"
PORT = 12000
SEAT_FILE = "seats.json"
lock = threading.Lock()

logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def load_seats():
    if os.path.exists(SEAT_FILE):
        with open(SEAT_FILE, "r") as f:
            return json.load(f)
    else:
        seats = {str(i): False for i in range(1, 6)}
        save_seats(seats)
        return seats

def save_seats(seats):
    tmp = SEAT_FILE + ".tmp"                   # ADDED: atomic write
    with open(tmp, "w") as f:
        json.dump(seats, f)
    os.replace(tmp, SEAT_FILE)

seats = load_seats()

def handle_client(conn, addr):
    try:                                       # ADDED: catch unexpected errors
        data = conn.recv(1024)
        if not data:
            return
        message = data.decode().strip()
        print("Request from", addr, ":", message)
        logging.info(f"{addr} -> {message}")

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

        if len(parts) == 2 and parts[0] == "CANCEL":   # ADDED: cancel handler
            seat_id = parts[1]
            if not seat_id.isdigit():
                conn.send("INVALID_SEAT_NUMBER".encode())
                return
            with lock:
                if seat_id not in seats:
                    response = "FAILED_INVALID_SEAT"
                elif not seats[seat_id]:
                    response = "FAILED_NOT_BOOKED"
                else:
                    seats[seat_id] = False
                    save_seats(seats)
                    response = "CANCELLED"
            conn.send(response.encode())
            logging.info(f"{addr} <- {response}")
            return

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

    except Exception as e:                     # ADDED
        logging.error(f"Error handling {addr}: {e}")
    finally:
        conn.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # ADDED
server_socket.bind((HOST, PORT))
server_socket.listen()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

print("Secure reservation server running on port", PORT)

while True:
    conn, addr = server_socket.accept()
    secure_conn = context.wrap_socket(conn, server_side=True)
    threading.Thread(
        target=handle_client,
        args=(secure_conn, addr)
    ).start()