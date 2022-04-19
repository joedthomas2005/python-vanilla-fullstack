httpCodes = {200: "OK", 400: "Bad Request", 404: "Not Found", 
405:"Method Not Allowed",500: "Internal Server Error"}

class httpRequest:
    '''
    This class's constructor splits apart a given HTTP request and stores its method (GET, POST, PUT, HEAD etc), 
    resource requested, the HTTP protocol used (HTTP/1.0 HTTP/1.1 etc) and any parameters in the request (additional pieces of 
    data placed after a ? in the URL and separated with & characters).
    '''
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
    '''
    Construct a valid structured HTTP response with a given status code (A dictionary containing them is at the top of the file 
    this is declared in). 
    '''
    def __init__(self, status, data = "", type = "text/html", protocol = "HTTP/1.1"):
        '''
        Construct a valid structured HTTP response with a given status code (A dictionary containing them is at the top of the file 
        this is declared in) and any extra data required.
        '''
        self.headers = {}
        self.headers["Content-type"] = type
        self.headers["Content-Length"] = len(data.encode())

        self.responseLine = f"{protocol} {status} {httpCodes[status]}"

        self.data = data
    
    def setHeader(self, key, value):
        '''
        Set a specified header to a specified value (these give extra data to the browser about the response).
        '''
        self.headers[key] = value
    
    def build(self):
        '''
        Construct the request and return it as a raw string.
        '''
        text = self.responseLine + "\n"
        for key in self.headers.keys():
            text += f"{key}: {self.headers[key]}\n"
        text += "\n" + self.data
        return text

