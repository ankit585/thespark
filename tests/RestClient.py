import httplib2
import urllib

class RestClient: 
  """ A simple REST Client for making REST calls for regressions """

  (GET,POST,PUT,DELETE) = ("GET","POST","PUT","DELETE")

  def __init__(self,base_url):
     self.handle = httplib2.Http(".cache")
     self.base_url   = base_url
     

  def request(self,uri,type,data=None):
     url = self.base_url + uri
     resp = 0
     content = ""
  #   print url + " :: " + data 
     if type == RestClient.GET or type == RestClient.DELETE: 
         (resp, content) = self.handle.request(url, type)
     else:
         (resp, content) = self.handle.request(url,type,body = data)
     return (resp.status,content.decode('utf-8')) 
  
