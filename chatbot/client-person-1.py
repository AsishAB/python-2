# Create a chatbot, that continues communication between client and server as long as one of them says 'bye'

import socket

def client():
    clientSocket = socket.socket()
    host = socket.gethostname()

    port = 12345

    clientSocket.connect((host, port))
    #print(clientSocket.recv(20))


    while True:
        msg = input("Enter your message from client ")

        clientSocket.send(msg.encode())
        data = clientSocket.recv(1024).decode()
        if data == 'bye':
            clientSocket.close()
            break
        else:

            print(data)
            continue

client()