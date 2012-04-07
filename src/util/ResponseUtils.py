import web
import json
import

import util.Callable

class ResponseUtils():

    def createResponse(status, result, serialize, format="json"):
        """ Create and format a response
            Available formats: JSON ('json'), XML ('xml')
        """
        format = format.lower()
        
        # set header
        if format == "json":
            web.header('Content-Type', 'application/json')
        elif format == "xml":
            web.header('Content-Type', 'application/xml')
        else:
            format = "json"
            web.header('Content-Type', 'application/json')
        
        
        if status == False:
            status = 'failure'
        else:
            status = 'success'
        
        
        if serialize:
            res = [i.serialize for i in result]
        else:
            res = result
        
        
        response = json.dumps({'status':status,'data':res})
        input = web.input(callback="")
        if input.callback:
            response= input.callback + '(' + response + ')'
        return response;

    createResponse = util.Callable.Callable(createResponse)
