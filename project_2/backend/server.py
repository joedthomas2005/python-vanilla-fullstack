import socket
import actions

import modules.httpFormatter as httpFormatter
import modules.requestHandler as requestHandler


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 3001))

print("listening")
server.listen(100)

#Should make a better way of adding handlers than this horrible block

handler = requestHandler.requestHandler()
handler.setSiteDir("site")
handler.setDefault(handler.loadfilesafe)
handler.addHandler("GET", "error.html", lambda x,y: handler.forbidden())
handler.addHandler("GET", "", lambda x,y: handler.loadfilesafe("index.html"))
handler.addHandler("GET", "search", actions.search)
handler.addHandler("GET", "posts", actions.readPost)
handler.addHandler("POST", "posts", actions.new)
handler.addHandler("DELETE", "posts", actions.delete)
handler.setCORSmethods("posts", "GET", "POST", "DELETE")
handler.setCORSheaders("posts", "Content-Type")
handler.setCORSmethods("search", "GET")

while True:

    c, addr = server.accept()
    data = c.recv(1024).decode()

    request = httpFormatter.httpRequest(data)
    print(f"""{request.method} REQUEST FOR {request.resource} 
    WITH PARAMS {request.params} AND BODY {request.body}""")

    response = handler.handle(request)
    
    c.send(response.build())
    c.close()
    
