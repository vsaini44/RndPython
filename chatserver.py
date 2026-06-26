import socket

# Create socket
server = socket.socket()

# Bind to localhost and port 9040
server.bind(("localhost", 9040))

# Listen for one client
server.listen(1)

print("Waiting for client...")

client_socket, address = server.accept()

print("Client connected:", address)

while True:
    # Receive message from client
    message = client_socket.recv(1024).decode()

    if message == "exit":
        print("Client disconnected.")
        break

    print("Client:", message)

    # Send reply
    reply = input("Server: ")

    client_socket.send(reply.encode())

    if reply == "exit":
        break

client_socket.close()
server.close()
