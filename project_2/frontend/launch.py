import socket
import httpFormatter
import requestHandler

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind('', 80)

print("HTTP server live")
server.listen(100)

handler = requestHandler.requestHandler()


while True:
    
    c, addr = server.accept()
    data = c.recv(1024).decode()
    req = httpFormatter.httpRequest(data)
    
    res = handler.handle(f"{req.method} {req.resource}", req.params)
    
    c.send(res.build().encode())
    c.close()