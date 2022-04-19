import httpClasses

class requestHandler:
    def __init__(self):
        self.requests = {}
    
    def addHandler(self, request, handler):
        self.requests[request] = handler
    
    def handle(self, request, params):
        if(request in self.requests.keys()):
            response = self.requests[request](params)
        elif "GET " in request:
            response = self._error(404)
        elif "POST " in request:
            response = self._error(405)
        else:
            response = self._error(400)

        response.setHeader("Access-Control-Allow-Origin", "*")
        return response
        
    def _error(self, status):
        return httpClasses.httpResponse(status)



