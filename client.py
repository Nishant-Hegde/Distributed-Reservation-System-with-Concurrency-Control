import socket
import ssl

HOST = "127.0.0.1"
PORT = 12000

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
secure_socket = context.wrap_socket(client_socket, server_hostname=HOST)

try:
    secure_socket.connect((HOST, PORT))

    print("------ Reservation Client ------")
    print("1. Reserve Seat")
    print("2. Check Seat Status")

    choice = input("Enter choice: ")

    if choice == "2":
        message = "STATUS"

    elif choice == "1":
        seat = input("Enter seat number (1-5): ")

        if not seat.isdigit():
            print("Invalid seat number")
            secure_socket.close()
            exit()

        message = f"RESERVE {seat}"

    else:
        print("Invalid choice")
        secure_socket.close()
        exit()

    secure_socket.send(message.encode())

    response = secure_socket.recv(1024)

    print("Server response:", response.decode())

finally:
    secure_socket.close()