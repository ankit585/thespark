import httplib2
import urllib
import base64
class RestClient: 
  """ A simple REST Client for making REST calls for regressions """

  (GET,POST,PUT,DELETE) = ("GET","POST","PUT","DELETE")

  def __init__(self,base_url):
     self.handle = httplib2.Http(".cache")
     self.base_url   = base_url
     self.headers = ''
 
  def authenticate(self,user,password,url):
     auth = base64.encodestring( user + ':' + password )
     resp, content = self.handle.request(url,'GET',headers = { 'Authorization' : 'Basic ' + auth })
     self.headers = {'Cookie': resp['set-cookie']}

  def request(self,uri,type,data=None):
     url = self.base_url + uri
     resp = 0
     content = ""
     if type == RestClient.GET or type == RestClient.DELETE: 
         (resp, content) = self.handle.request(url, type, headers = self.headers)
     else:
         (resp, content) = self.handle.request(url,type,body = data, headers = self.headers)
     return (resp.status,content.decode('utf-8')) 


if __name__ == '__main__': 
 
   host = 'http://babyalong-dr.eglbp.corp.yahoo.com'
   data = ""
   uri  ='/api/reports/campaigns?dummy=1&startDate=20120109&endDate=20120523&tz=IST&offset=0&startRow=1&rowCount=10&orderBy=startDate&order=desc'
   
   conn = RestClient(host)
   conn.authenticate('admin','admin','http://babyalong-dr.eglbp.corp.yahoo.com:4080/ycreativeapi/login')
   (resp , content) = conn.request(uri,RestClient.GET,data)
   print content
