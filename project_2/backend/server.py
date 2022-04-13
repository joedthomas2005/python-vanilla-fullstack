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

    if request.method == "GET":
        if request.resource == "search":

            try:
                queryTerm = request.params["query"]
                count = int(request.params["count"])

                items = []
                for i in range(count):
                    items.append({
                        "number": i,
                        "query": queryTerm
                    })
                
                response = httpClasses.httpResponse("text/html", 200, json.dumps(items))
                response.setHeader("Access-Control-Allow-Origin","*")
            except:
                response = httpClasses.httpResponse("text/html", 400)
            
        else:
            response = httpClasses.httpResponse("text/html", 404)
        

        c.send(response.build().encode())