import socket
import threading
import random

HOST = "127.0.0.1"
PORT = 12000


def client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    seat = random.randint(1, 5)
    message = f"RESERVE {seat}"

    s.send(message.encode())

    response = s.recv(1024)
    print("Seat", seat, "->", response.decode())

    s.close()


threads = []

for i in range(10):  # 10 concurrent clients
    t = threading.Thread(target=client)
    threads.append(t)
    t.start()

for t in threads:
    t.join()