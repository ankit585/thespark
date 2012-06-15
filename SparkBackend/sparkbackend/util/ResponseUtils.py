import web
import json
import XMLDict
from pyramid.response import Response
import pprint
from sparkbackend.util.Callable import Callable

class ResponseUtils():

    def createResponse(status,code, result, serialize,request ,format="json",header=None):
        """ Create and format a response
            Available formats: JSON ('json'), XML ('xml')
        """
        format = format.lower()
        
        # set status
        if status == False:
            status = 'failure'
        else:
            status = 'success'
        
        if serialize:
            output = [i.serialize for i in result]
        else:
            output = result
        
        res = Response('')

        # set header
        if format == "xml":
            res.content_type = 'application/xml'
        else: # default - format = "json"
            format = "json"
            res.content_type = 'application/json'

        if header != None:
           res.headerlist = header

        if format == "xml":
            response = XMLDict.convert_dict_to_xml({'response': {'status':status,'code':code, 'data':output}})
        else: # default - format = "json":
            response = json.dumps({'status':status,'code':code, 'data':output})

        callback = request.params.get('callback',None) 
        if callback:
            response = callback + '(' + response + ')'
            res.text = response 
        else:
            res.body = response

        return res

    createResponse = Callable(createResponse)

