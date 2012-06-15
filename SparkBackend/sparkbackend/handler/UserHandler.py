from  sparkbackend.models.User import User
from  sparkbackend.models.EmailCode import EmailCode
from  sparkbackend.util.DBUtils import DBUtils
from  sparkbackend.util.ResponseUtils import ResponseUtils
from  sparkbackend.util.SystemUtils import SystemUtils
from  sparkbackend.util.EmailUtils import EmailUtils
import pprint
import sys
import json
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.security import forget
import hashlib
import traceback

class UserHandler(object):

    def __init__(self,request):
        #init DB session
        self.request = request
        self.url_params    = request.params
        self.session = DBUtils.getSession()
        # get format from url parameters
        url_params  = request.params
        self.format = self.url_params.get('format')
        if not self.format:
           self.format = 'json'
        # get and parse raw post data
        data = request.body
        self.data = dict([part.split('=') for part in data.split('&')]) if data != "" else {}

    #POST
    def user_login(self):
        """Check if user can login
        """
        code = "0" 
        if 'form.submitted' in self.request.params:
            if len(self.data['user']) > 0 and len(self.data['password']) > 0:
               id = self.data['user']
               salt = ""
               password = hashlib.md5(salt + self.data['password']).hexdigest()
               user = self.session.query(User).filter_by(userID=id).first()
               if user.password == password:
                 headers = remember(self.request,id)
                 return HTTPFound(location = "/",
                             headers = headers)
               else:
                 status = False
                 response = "Login Failed"
            else: 
               status = False
               response = "Login Failed"
            return ResponseUtils.createResponse(status,code, response, False,self.request, self.format,headers)
        return dict(
            message = '',
            url = self.request.application_url + '/login',
            came_from = self.request.application_url + '/',
            user = '',
            password = ''
        )
    

    #GET      
    def user_get(self):
        """ Check if a userID exists
        """
        code = 0
        user = None
        try:
           uid = self.request.matchdict['userID'] 
           user = self.session.query(User).filter_by(userID=uid).first()
           if user != None:
              status = True
              response = "user exists"
           else:
              status = False
              code = "005"
              response = "no such user found"
        except KeyError:
           status = False
           code   = "001"
           response= "required fields missing"
        except:  
           status = False
           code = "004"
           response = "internal error"
           exc_type, exc_value, exc_traceback = sys.exc_info()
           lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
           print ''.join('*** ' + line for line in lines) 
     
        return ResponseUtils.createResponse(status,code, response, False,self.request, self.format)

    #GET      
    def user_email_get(self):
        """ Check if an email exists
        """
        code = "0"
        user = None
        try: 
           uid = self.request.matchdict['email'] 
           user = self.session.query(User).filter_by(email=uid).first()
           if user != None:
              status = True
              response = "email exists"
           else:
              status = False
              code = "006"
              response = "no such email found" 
        except KeyError:
           status = False
           code   = "001"
           response= "required fields missing"
        except:  
           status = False
           code = "004"
           response = "internal error"
           exc_type, exc_value, exc_traceback = sys.exc_info()
           lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
           print ''.join('*** ' + line for line in lines) 
     
        return ResponseUtils.createResponse(status,code, response, False,self.request, self.format)


    #POST
    def register(self):
        """Create a new account
        """
        code = "0"
        try:    
            if len(self.data['userID']) > 0 and len(self.data['password']) > 0 and len(self.data['email']) > 0 and len(self.data['firstName']) > 0 and len(self.data['lastName']) > 0:

               if self.session.query(User).filter_by(email=self.data['email']).first():
                   response = "email is already registered"
                   code     = "003"
                   status   = False
               elif self.session.query(User).filter_by(userID=self.data['userID']).first():
                   response = "userID is already registered"
                   code     = "002"
                   status   = False
               else:
                   # create database object
                   salt = "" #need to get salt from secret config
                   password = hashlib.md5(salt + self.data['password']).hexdigest()
                   user = User(self.data['userID'], password ,self.data['email'],self.data['firstName'],self.data['lastName'])
                   self.session.add(user)
                   self.session.flush()
                   secret = SystemUtils.createRandomString()
                   email_code = EmailCode(user.id,secret)
                   self.session.add(email_code)                
                   # send a mail to user
                   EmailUtils.sendRegistrationMail(self.data['email'],self.data['firstName'],user.id,secret)
          
                   # commit change to DB
                   self.session.commit()

                   status = True
                   response = "user registered successfully"
            else:
               response = "required fields missing"
               code     = "001"
               status   = False
        except KeyError:
           status = False
           code   = "001"
           response= "required fields missing"
        except:  
           status = False
           code = "004"
           response = "internal error"
           exc_type, exc_value, exc_traceback = sys.exc_info()
           lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
           print ''.join('*** ' + line for line in lines) 

        return ResponseUtils.createResponse(status,code, response, False,self.request, self.format)

    #PUT 
    def reset_password(self):
        """Update an existing password
        """
        code = "0"
        try: 
           uid = self.request.matchdict['userID'] 
           user = self.session.query(User).filter_by(userID=uid).first()
           if len(self.data['old_password']) > 0 and len(self.data['new_password']) > 0:
               if len(uid) <= 0:
                  response = "required fields missing"
                  status   = False
                  code = "001"
               elif user == None:
                  response = "no such user found"
                  code = "005"
                  status   = False
               else:
                   # create database object
                  salt = ""
                  old_password = hashlib.md5(salt + self.data['old_password']).hexdigest()
                  if user.password == old_password:
                      user.password = self.data['new_password']
                      user.password = hashlib.md5(salt + self.data['new_password']).hexdigest()
                      self.session.add(user)
                      response = "password reset successful"
                      # commit change to DB                
                      self.session.commit()
                      status = True
                  else:
                      status = False
                      response = "existing password is incorrect"   
           else:
               response = "required fields missing"
               code = "001"
               status   = False
        except KeyError:
           status = False
           code   = "001"
           response= "required fields missing"
        except:  
           status = False
           code = "004"
           response = "internal error"
           exc_type, exc_value, exc_traceback = sys.exc_info()
           lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
           print ''.join('*** ' + line for line in lines) 
        
        return ResponseUtils.createResponse(status,code , response, False,self.request, self.format)

    #DELETE 
    def user_delete(self):
        """Delete an existing user account
        """
        code = "0"
        try: 
           uid = self.request.matchdict['userID'] 
           user = self.session.query(User).filter_by(userID=uid).first()
           if len(self.data['password']) > 0:
               if len(uid) <= 0:
                  response = "required fields missing"
                  code = "001"
                  status   = False
               elif user == None:
                  response = "no such user found"
                  code = "005"
                  status   = False
               else:
                   # create database object
                  salt = ""
                  password = hashlib.md5(salt + self.data['password']).hexdigest()
                  if user.password == password:
                      self.session.delete(user)
                      response = "user deleted"
                      # commit change to DB                
                      self.session.commit()
                      status = True
                  else:
                      status = False
                      response = "existing password is incorrect"   
           else:
               response = "required fields missing"
               code = "001"
               status   = False
        except KeyError:
           status = False
           code   = "001"
           response= "required fields missing"
        except:  
           status = False
           code = "004"
           response = "internal error"
           exc_type, exc_value, exc_traceback = sys.exc_info()
           lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
           print ''.join('*** ' + line for line in lines) 
        

        return ResponseUtils.createResponse(status,code, response, False, self.request,self.format)

