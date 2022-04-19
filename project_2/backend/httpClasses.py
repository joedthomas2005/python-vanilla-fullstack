httpCodes = {200: "OK", 400: "Bad Request", 404: "Not Found", 
405:"Method Not Allowed",500: "Internal Server Error"}

class httpRequest:

    def __init__(self, data):
        self.rawData = data
        try:
            lines = data.split("\n")
        
            print(lines[0])
            requestLine = lines[0].split(" ")
            self.method = requestLine[0]
            self.resource = requestLine[1][1:]
            self.protocol = requestLine[2]
            self.paramLine = ""
            if "?" in self.resource:
                self.paramLine = self.resource.split("?")[1]
                self.resource = self.resource.split("?")[0]
            
            self.params = {}
            if(self.paramLine):
                for param in self.paramLine.split("&"):
                    print(param)
                    self.params[param.split("=")[0]] = param.split("=")[1]

        except:

            self.method = "NULL"
            self.resource = data
            self.paramLine = "NULL"
            self.protocol = "NULL"
            self.params = {}

class httpResponse:

    def __init__(self, status, type = "text/html", data = "", protocol = "HTTP/1.1"):
        
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