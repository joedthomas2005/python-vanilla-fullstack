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

        self.text = self.responseLine + "\n"

        for header in self.headers.keys():
            self.text += f"{header}: {self.headers[header]}\n"
        
        self.text += data

req = requests.get("https://www.randomlists.com/data/words.json")

words = json.loads(req.text)["data"]
 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            index = int(urlParams[1])
            if(index >= len(words)):
                c.send("NULL".encode())
            else:
                response = httpResponse("text/html", 200, words[index])
                c.send(response.text.encode())
    c.close()
 

