import socket

s = socket.socket()

host = socket.gethostname()

port = 12345

s.connect((host, port))

print(s.recv(10)) # only receive 10 bytes of data from server