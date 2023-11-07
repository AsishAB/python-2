# import socket
#
# s = socket.socket()
#
# host = socket.gethostname()
#
# port = 12345
#
# s.connect((host, port))
#
# print(s.recv(10)) # only receive 10 bytes of data from server
#
# msg = b"Hello, good morning from"
# s.send(msg)


import socket

def client():
    clientSocket = socket.socket()
    host = socket.gethostname()

    port = 12345

    clientSocket.connect((host, port))
    #print(clientSocket.recv(20))

    msg = "Hello,Good Morning"
    clientSocket.send(msg.encode())
    data = clientSocket.recv(1024).decode()
    print(data)
    clientSocket.close()

client()