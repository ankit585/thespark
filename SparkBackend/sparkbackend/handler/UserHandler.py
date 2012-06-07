from  sparkbackend.models.User import User
from  sparkbackend.util.DBUtils import DBUtils
from  sparkbackend.util.ResponseUtils import ResponseUtils
import pprint
import sys
import json
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.security import forget


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
         
        if 'form.submitted' in self.request.params:
            if len(self.data['user']) > 0 and len(self.data['password']) > 0:
               id = self.data['user']
               password = self.data['password']
               cit = self.session.query(User).filter_by(userID=id).first()
               if cit.password == password:
                 headers = remember(self.request,id)
                 return HTTPFound(location = "/",
                             headers = headers)
               else:
                 status = False
                 response = "Login Failed"
            else: 
               status = False
               response = "Login Failed"
            return ResponseUtils.createResponse(status, response, False,self.request, self.format,headers)
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
        cits = None
        cid = self.request.matchdict['userID'] 
        cits = self.session.query(User).filter_by(userID=cid).first()
        if cits != None:
           status = True
           response = "User Exists"
        else:
           status = False
           response = "User not Found" 
     
        return ResponseUtils.createResponse(status, response, False,self.request, self.format)

    #POST
    def register(self):
        """Create a new account
        """
            
        # validate
        if len(self.data['userID']) > 0 and len(self.data['password']) > 0 and len(self.data['email']) > 0:
            # create database object
            cit = User(self.data['userID'], self.data['password'],self.data['email'])
            self.session.add(cit)
            response = "Record created successfully"
            
            # commit change to DB
            self.session.commit()
            status = True
        else:
            response = "User ID or password or email missing"
            status   = False

        return ResponseUtils.createResponse(status, response, False,self.request, self.format)

    #PUT 
    def reset_password(self):
        """Update an existing password
        """
        
        cid = self.request.matchdict['userID'] 
        # validate
        if len(self.data['old_password']) > 0 and len(self.data['new_password']) > 0:
            if len(cid) <= 0:
                response = "Missing parameter (userID to be updated)"
                status   = False
            else:
                # create database object
                cit = self.session.query(User).filter_by(userID=cid).first()
                if cit.password == old_password:
                   cit.password = self.data['new_password']
                   self.session.add(cit)
                   response = "Record updated successfully"
                   # commit change to DB                
                   self.session.commit()
                   status = True
                else:
                   status = False
                   response = "Old password didn't match"   
        else:
            response = "Old password or new password missing"
            status   = False

        return ResponseUtils.createResponse(status, response, False,self.request, self.format)

    #DELETE 
    def user_delete(self):
        """Delete an existing user account
        """
        
        cid = self.request.matchdict['userID'] 
        # validate
        if len(cid) <= 0:
            response = "Missing parameter (userID to be deleted)"
            status   = False
        else:
            # create database object
            cit = self.session.query(User).filter_by(userID=cid).first()
            self.session.delete(cit)
            
            # commit changes to DB
            self.session.commit()
            status   = True
            response = "Record deleted successfully"

        return ResponseUtils.createResponse(status, response, False, self.request,self.format)

