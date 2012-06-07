from  sparkbackend.models.Citation import Citation
from  sparkbackend.util.DBUtils import DBUtils
from  sparkbackend.util.ResponseUtils import ResponseUtils
import pprint
import sys
import json
from pyramid.security import Authenticated
from pyramid.security import authenticated_userid

class CitationHandler(object):

    def __init__(self,request):
        #init DB session
        self.request = request
        data    = request.body
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

    def citation_get(self):
        """Display a single citation 
        """
        owner = authenticated_userid(self.request)
        cits = None
        cid = self.request.matchdict['id'] 
        cits = self.session.query(Citation).filter_by(id=cid).all()
        print " Got Owner " + owner
        return ResponseUtils.createResponse(True, cits, True,self.request, self.format)

    def citation_index(self):
        """Display a full list of citation if no ID specified
        """
        cits = None
        cits = self.session.query(Citation).order_by(Citation.id).all()

        return ResponseUtils.createResponse(True, cits, True, self.request,self.format)


    def citation_post(self):
        """Create a new citation
        """
            
        # validate
        if len(self.data['content']) > 0 and len(self.data['url']) > 0:
            # create database object
            cit = Citation(self.data['content'], self.data['url'])
            self.session.add(cit)
            response = "Record created successfully"
            
            # commit change to DB
            self.session.commit()
            status = True
        else:
            response = "Content or URL missing"
            status   = False

        return ResponseUtils.createResponse(status, response, False, self.request,self.format)


    def citation_put(self):
        """Update an existing citation
        """
         
        cid = self.request.matchdict['id'] 
        # validate
        if len(self.data['content']) > 0 and len(self.data['url']) > 0:
            if len(cid) <= 0:
                response = "Missing parameter (id to be updated)"
                status   = False
            else:
                # create database object
                cit = self.session.query(Citation).filter_by(id=cid).first()
                cit.content = self.data['content']
                cit.url     = self.data['url']
                self.session.add(cit)
                response = "Record updated successfully:" + owner

                # commit change to DB                
                self.session.commit()
                status = True
        else:
            response = "Content or URL missing:" + owner
            status   = False

        return ResponseUtils.createResponse(status, response, False,self.request, self.format)


    def citation_delete(self):
        """Delete an existing citation
        """
        
        cid = self.request.matchdict['id'] 
        # validate
        if len(cid) <= 0:
            response = "Missing parameter (id to be deleted)"
            status   = False
        else:
            # create database object
            cit = self.session.query(Citation).filter_by(id=cid).first()
            self.session.delete(cit)
            
            # commit changes to DB
            self.session.commit()
            status   = True
            response = "Record deleted successfully"

        return ResponseUtils.createResponse(status, response, False, self.request,self.format)

