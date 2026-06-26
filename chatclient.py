import socket

# Create socket
client = socket.socket()

# Connect to server
client.connect(("localhost", 9040))

print("Connected to server!")

while True:
    # Send message
    message = input("Client: ")

    client.send(message.encode())

    if message == "exit":
        break

    # Receive reply
    reply = client.recv(1024).decode()

    if reply == "exit":
        print("Server disconnected.")
        break

    print("Server:", reply)

client.close()
