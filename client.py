import socket

HOST = "127.0.0.1"
PORT = 12000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

seat = input("Enter seat number to reserve (1-5): ")
message = f"RESERVE {seat}"

client_socket.send(message.encode())

response = client_socket.recv(1024)
print("Server response:", response.decode())

client_socket.close()
