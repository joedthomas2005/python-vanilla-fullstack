import modules.httpFormatter as httpFormatter
class requestHandler:
    '''
    This class handles given requests by executing specified functions associated with the request string. Request strings are 
    structured as "METHOD resource" (the protocol is not necessary). Functions associated with these strings must return an instance 
    of httpFormatter.httpResponse and must also take in exactly 1 parameter which will constitute a dictionary containing all the URL parameters 
    in the request.
    '''
    def __init__(self):
        self.requests = {}
    
    def addHandler(self, method, resource, handler):
        '''
        Associate a request string with a function to call when that request is handled.
        The first parameter should be the request string (e.g. "GET api") and the second should 
        be a function to run when that request is handled. This should be passed without parentheses 
        (i.e. foo not foo()). 
        '''
        self.requests[f"{method} {resource}"] = handler
    
    def handle(self, method, resource, params):
        '''
        Run the handler function associated with the given request string. The strings must match exactly.
        '''
        request = f"{method} {resource}"
        if(request in self.requests.keys()):
            response = self.requests[request](params)
        elif "GET " in request:
            response = self.__error(404)
        elif "POST " in request:
            response = self.__error(405)
        else:
            response = self.__error(400)

        response.setHeader("Access-Control-Allow-Origin", "*")
        return response
        
    def __error(self, status):
        return httpFormatter.httpResponse(status)



