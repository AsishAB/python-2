# Create a chatbot, that continues communication between client and server as long as one of them says 'bye'

import socket

def server():
    serverSocket = socket.socket()
    host = socket.gethostname()

    port = 12345

    serverSocket.bind((host,port))

    serverSocket.listen(10)

    client,address = serverSocket.accept()
    print("Got Connection request from",address)

    while True:
        msg = input("Enter response from server ")
        data = client.recv(1024).decode()
        if not data:
            break
        print(data)
        client.send(msg.encode())
        if data == 'bye':
            break
        else:
            continue

server()