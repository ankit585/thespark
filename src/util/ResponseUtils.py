import web
import json 

import util.Callable

class ResponseUtils():
    
     def createResponse(st,result,serialize):
        web.header('Content-Type', 'application/json')

        status = 'success'
        if st == False:
           status = 'failure'
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
