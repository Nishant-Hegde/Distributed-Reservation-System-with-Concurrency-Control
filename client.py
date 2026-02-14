import socket

HOST = "127.0.0.1"   # server address
PORT = 12000

# Create TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((HOST, PORT))

# Take input
message = input("Enter message: ")

# Send data
client_socket.send(message.encode())

# Receive response
data = client_socket.recv(1024)
print("From server:", data.decode())

# Close socket
client_socket.close()
