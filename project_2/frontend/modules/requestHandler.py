import modules.httpFormatter as httpFormatter
import os.path
class requestHandler:
    '''
    This class handles given requests by executing specified functions associated with the request string. Request strings are 
    structured as "METHOD resource" (the protocol is not necessary). Functions associated with these strings must return an instance 
    of httpFormatter.httpResponse and must also take in exactly 1 parameter which will constitute a dictionary containing all the URL parameters 
    in the request.
    '''
    def __init__(self):
        self.requests = {}
        self.CORSmethods = {}
        self.CORSheaders = {}
        self.default = self.loadfileunsafe
        self.siteDir = "./"

    def setDefault(self, function):
        self.default = function

    def setCORSmethods(self, resource, *methods):
        self.CORSmethods[resource] = ','.join(methods).upper()

    def setCORSheaders(self, resource, *headers):
        self.CORSheaders[resource] = ','.join(headers)

    def setSiteDir(self, directory):
        self.siteDir = f"{directory}/"

    def addHandler(self, method, resource, handler):
        '''
        Associate a request string with a function to call when that request is handled.
        The first parameter should be the request method (e.g. GET), the second should 
        be the resource (e.g. home) and the third should be a function to run when that 
        request is handled. This should be passed without parentheses 
        (i.e. foo not foo()). 
        '''
        self.requests[f"{method} {resource}"] = handler
    
    def handle(self, request):
        '''
        Run the handler function associated with the given request string. The strings must match exactly.
        '''
        requestString = f"{request.method} {request.resource}"
        
        if(requestString in self.requests.keys()):
            response = self.requests[requestString](request.params, request.body)

        elif request.method == "GET":
            if(os.path.exists(self.siteDir + request.resource)):
                response = self.default(request.resource)
            else:
                response = self.error(404)
        
        elif request.method == "OPTIONS":

            if(request.resource in self.CORSmethods.keys()):
                response = httpFormatter.httpResponse(200)
                response.setHeader("Allow", self.CORSmethods[request.resource])
            
                if(request.resource in self.CORSheaders.keys()):
                    response.setHeader("Access-Control-Allow-Headers", self.CORSheaders[request.resource])
            
            else:
                response = self.error(500)

        elif request.method == "POST":
            response = self.error(405)
        
        else:
            response = self.error(400)

        response.setHeader("Access-Control-Allow-Origin", "*")
        return response
        
    def error(self, status):
        return httpFormatter.httpResponse(status)

    def loadfilesafe(self, resource):

        if ".." in resource or resource[0] == "/":
            return self.error(403)

        path = self.siteDir + resource
        print("loading " + path)
        file = open(path, 'rb')
        data = file.read()

        return httpFormatter.httpResponse(200, data, requestHandler.getMimeType(path))


    def notfound(self, resource):
        return self.error(404)

    def forbidden(self, resource):
        return self.error(403)

    def loadfileunsafe(self, resource):
        
        path = self.siteDir + resource
        file = open(path, 'rb')
        data = file.read()
        return httpFormatter.httpResponse(200, data, requestHandler.getMimeType(path))

    def getMimeType(path):

        if(path.split(".")[-1] == "js"):
            return "text/javascript"
        elif(path.split(".")[-1] == "css"):
            return "text/css"
        return "text/html"