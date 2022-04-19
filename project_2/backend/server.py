import socket
import json
import httpClasses
import posts

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

                databaseEntries = posts.search(queryTerm, count)
                
                items = []
                for i in range(len(databaseEntries)):
                    items.append({
                        "number": i,
                        "query": queryTerm,
                        "title": databaseEntries[i][1],
                        "body": posts.readPost(databaseEntries[i][2])
                    })
                
                response = httpClasses.httpResponse(200, "text/html", json.dumps(items))
                response.setHeader("Access-Control-Allow-Origin","*")

            except:
                response = httpClasses.httpResponse(400)
        
        elif request.resource == "posts":
            try:
                postId = int(request.params["id"])
                responseData = posts.readPostById(postId)

                if(responseData):
                    response = httpClasses.httpResponse(200, "text/html", json.dumps(responseData))
                    response.setHeader("Access-Control-Allow-Origin", "*")
                else:
                    response = httpClasses.httpResponse(404)
                    print(404)

            except ValueError as v:
                response = httpClasses.httpResponse(400)
                print(400)
            
            except KeyError as k:
                response = httpClasses.httpResponse(400)
                print(400)
                 
        else:
            response = httpClasses.httpResponse(404)
            print(404)        

        c.send(response.build().encode())
    
    elif request.method == "POST":
        print("Post Request")
        response = httpClasses.httpResponse(405)
        print(405)
        c.send(response.build().encode())

    else:
        response = httpClasses.httpResponse(400)
        print(400)
        c.send(response.build().encode())
