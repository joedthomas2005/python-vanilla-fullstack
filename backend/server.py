import socket
import json
import requests

httpCodes = {200:"OK", 401:"Unauthorized", 404:"Not Found", 500:"Internal Server Error"}
class httpRequest:

    def __init__(self, data):
        self.rawData = data

        lines = data.split("\n")
        
        print(lines[0])
        requestLine = lines[0].split(" ")
        self.method = requestLine[0]
        self.resource = requestLine[1][1:]
        self.protocol = requestLine[2]

class httpResponse:

    def __init__(self, type, status, data = "", protocol = "HTTP/1.1"):
        
        self.headers = {}
        self.headers["Content-type"] = type
        self.headers["Content-Length"] = len(data.encode())

        self.responseLine = f"{protocol} {status} {httpCodes[status]}"

        self.data = data
    
    def setHeader(self, key, value):
        self.headers[key] = value
    
    def build(self):
        text = self.responseLine + "\n"
        for key in self.headers.keys():
            text += f"{key}: {self.headers[key]}\n"
        text += "\n" + self.data
        return text
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
server.bind(('', 3000))

print("listening")
server.listen(10)
 
while True:

    c, addr = server.accept()
     
    data = c.recv(1024).decode()
    print("new request")
     
    request = httpRequest(data)
    print(f"{request.protocol} {request.method} REQUEST FOR {request.resource}")
     
    if(request.method == "GET"):
        urlParams = request.resource.split("/")
        
        if(urlParams[0] == "words"):

            words = open("words.txt", "r").readlines()
            index = int(urlParams[1])
            if(index >= len(words)):
                response = httpResponse("text/html", 404)
                response.setHeader("Access-Control-Allow-Origin","*")
                c.send(response.build().encode())
            else:
                response = httpResponse("text/html", 200, words[index])
                response.setHeader("Access-Control-Allow-Origin","*")
                c.send(response.build().encode())
    c.close()
 

