# import socket
# s = socket.socket()
# host = socket.gethostname()
#
# port = 12345 # Same port as client
#
# s.bind((host, port))
# s.listen(10)
#
# while True:
#     client, address = s.accept()
#     print("Got connection request from  ", address)
#     client.send(b"Acknowledged")
#     client.close()


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
        data = client.recv(1024).decode()
        if not data:
            break
        print(data)
        msg = input("->")
        client.send(msg.encode())
        #client.close()

server()