import socket

HOST = "127.0.0.1"
PORT = 12000

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    seat = input("Enter seat number (1-5) OR type STATUS: ")

    if seat.upper() == "STATUS":
        message = "STATUS"
    else:
        message = f"RESERVE {seat}"

    client_socket.send(message.encode())

    response = client_socket.recv(1024)
    print("Server response:", response.decode())

except Exception as e:
    print("Connection error:", e)

finally:
    client_socket.close()