import socket
import actions
import sys

import modules.httpFormatter as httpFormatter
import modules.requestHandler as requestHandler


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 3001))

print("listening")
server.listen(100)

handler = requestHandler.requestHandler()
handler.setDefault(handler.loadfilesafe)
handler.addHandler("GET", "search", actions.search)
handler.addHandler("GET", "posts", actions.readPost)

while True:

    c, addr = server.accept()
    data = c.recv(1024).decode()

    request = httpFormatter.httpRequest(data)
    print(f"{request.method} REQUEST FOR {request.resource} WITH PARAMS {request.params}")

    response = handler.handle(request.method, request.resource, request.params)
    
    c.send(response.build().encode())
    c.close()
    