import socket
import threading
import random
import ssl

HOST = "127.0.0.1"
PORT = 12000


def client():

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    secure_socket = context.wrap_socket(s, server_hostname=HOST)

    secure_socket.connect((HOST, PORT))

    seat = random.randint(1, 5)
    message = f"RESERVE {seat}"

    secure_socket.send(message.encode())

    response = secure_socket.recv(1024)
    print("Seat", seat, "->", response.decode())

    secure_socket.close()


threads = []

for i in range(10):
    t = threading.Thread(target=client)
    threads.append(t)
    t.start()

for t in threads:
    t.join()