import socket

HOST = "127.0.0.1"
PORT = 12000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))

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
            client_socket.close()
            exit()

        message = f"RESERVE {seat}"

    else:
        print("Invalid choice")
        client_socket.close()
        exit()

    client_socket.send(message.encode())

    response = client_socket.recv(1024)

    print("Server response:", response.decode())

finally:
    client_socket.close()