import os.path
from types import FunctionType
import modules.httpFormatter as httpFormatter

class requestHandler:
    '''
    This class handles given requests by executing specified functions 
    associated with the request. Requests are described with a string structured 
    "METHOD resource". Functions associated with these request strings must return an instance 
    of httpFormatter.httpResponse and must also take in exactly 2 parameters 
    which will constitute a dictionary containing all the URL parameters and a string containing 
    the request body if it exists.
    '''
    def __init__(self):
        self.requests = {}
        self.CORSmethods = {}
        self.CORSheaders = {}
        self.default = self.loadfileunsafe
        self.siteDir = "./"

    def setDefault(self, defaultHandler: FunctionType) -> None:
        self.default = defaultHandler

    def setCORSmethods(self, resource: str, *methods: str) -> None:
        self.CORSmethods[resource] = ','.join(methods).upper()

    def setCORSheaders(self, resource: str, *headers: str) -> None:
        self.CORSheaders[resource] = ','.join(headers)

    def setSiteDir(self, directory: str) -> None:
        self.siteDir = f"{directory}/"

    def addHandler(self, method: str, resource: str, handler: FunctionType) -> None:
        '''
        Associate a request string with a function to call when that request is handled.
        The first parameter should be the request method (e.g. GET), the second should 
        be the resource (e.g. home) and the third should be a function to run when that 
        request is handled. This should be passed without parentheses 
        (i.e. foo not foo()). 
        '''
        self.requests[f"{method} {resource}"] = handler
    
    def handle(self, request: httpFormatter.httpRequest) -> httpFormatter.httpResponse:
        '''
        Run the handler function associated with the given request string. 
        The strings must match exactly.
        '''
        requestString = f"{request.method} {request.resource}"
        
        if requestString in self.requests:
            response = self.requests[requestString](request.params, request.body)

        elif request.method == "GET":
            if os.path.exists(self.siteDir + request.resource):
                response = self.default(request.resource)
            else:
                response = error(404)
        
        elif request.method == "OPTIONS":
            if request.resource in self.CORSmethods:
                response = httpFormatter.httpResponse(200)
                response.setHeader("Allow", self.CORSmethods[request.resource])
                
                if request.resource in self.CORSheaders:
                    response.setHeader("Access-Control-Allow-Headers", 
                    self.CORSheaders[request.resource])
            else:
                response = error(500)

        elif request.method == "POST":
            response = error(405)
        
        else:
            response = error(400)

        response.setHeader("Access-Control-Allow-Origin", "*")
        return response

    def loadfilesafe(self, resource: str) -> httpFormatter.httpResponse:

        if ".." in resource or resource[0] == "/":
            return error(403)

        path = self.siteDir + resource

        with open(path, 'rb') as file:
            data = file.read()

        return httpFormatter.httpResponse(200, data, getMimeType(path))  

    def loadfileunsafe(self, resource: str) -> httpFormatter.httpResponse:
        
        path = self.siteDir + resource
        with open(path, 'rb') as file:
            data = file.read()

        return httpFormatter.httpResponse(200, data, getMimeType(path))

def error(status: int) -> httpFormatter.httpResponse:
    return httpFormatter.httpResponse(status)

def notfound(_: str) -> httpFormatter.httpResponse:
        return error(404)

def forbidden(_: str) -> httpFormatter.httpResponse:
        return error(403)

def getMimeType(path: str) -> str:

    if path.split(".")[-1] == "js":
        return "text/javascript"
    if path.split(".")[-1] == "css":
        return "text/css"
    return "text/html"
