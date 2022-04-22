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
        self.default = self.loadfileunsafe
        self.siteDir = "./"

    def setDefault(self, function):
        self.default = function

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
    
    def handle(self, method, resource, params):
        '''
        Run the handler function associated with the given request string. The strings must match exactly.
        '''
        request = f"{method} {resource}"
        print("file path is " + self.siteDir + resource)
        if(request in self.requests.keys()):
            response = self.requests[request](params)
        elif os.path.exists(self.siteDir + resource):
            response = self.default(resource)
        elif "GET " in request:
            response = self.error(404)
        elif "POST " in request:
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
        file = open(path, 'r')
        data = file.read()
        return httpFormatter.httpResponse(200, data)

    def notfound(self, resource):
        return self.error(404)

    def forbidden(self, resource):
        return self.error(403)

    def loadfileunsafe(self, resource):
        
        path = self.siteDir + resource
        file = open(path, 'r')
        data = file.read()
        return httpFormatter.httpResponse(200, data)