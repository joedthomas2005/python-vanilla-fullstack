import socket
import json
import httpClasses

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 3000))

print("listening")
server.listen(10)

while True:

    c, addr = server.accept()
    data = c.recv(1024).decode()
    print("new request")
    request = httpClasses.httpRequest(data)
    print(f"{request.method} REQUEST FOR {request.resource} WITH PARAMS {request.params}")