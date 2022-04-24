import socket
import modules.httpFormatter as httpFormatter
import modules.requestHandler as requestHandler

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('', 80))

print("HTTP server live")
server.listen(100)

handler = requestHandler.requestHandler()
handler.setDefault(handler.loadfilesafe)
handler.setSiteDir("site")

handler.addHandler("GET", "", lambda x, y: handler.loadfilesafe("index.html"))

while True:
    
    c, addr = server.accept()
    data = c.recv(1024).decode()
    req = httpFormatter.httpRequest(data)
    
    try:
        res = handler.handle(req)
        c.send(res.build())
    except Exception as e:
        print(f"\033[91m{e}\033[0m")
        c.send(httpFormatter.httpResponse(500).build())
    c.close()
