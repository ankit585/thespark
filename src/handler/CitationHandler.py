import models.Citation
import util.DBUtils
import util.ResponseUtils
import json
import web

class CitationHandler():

    def __init__(self):
        #init DB session
        self.session = util.DBUtils.DBUtils.getSession()
        # get format from url parameters
        url_params  = web.input(format='')
        self.format = url_params.format
        # get and parse raw post data
        data = (web.data())
        self.data = dict([part.split('=') for part in data.split('&')]) if data != "" else {}


    def GET(self, cid):
        """Display a single citation or full list if no ID specified
        """
        cits = None
        
        if len(cid) <= 0:
            cits = self.session.query(models.Citation.Citation).order_by(models.Citation.Citation.id).all()
        else:
            cits = self.session.query(models.Citation.Citation).filter_by(id=cid).all()

        return util.ResponseUtils.ResponseUtils.createResponse(True, cits, True, self.format)



    def POST(self, uselessvar):
        """Create a new citation
            uselessvar is simply a placeholder
        """
            
        # validate
        if len(self.data['content']) > 0 and len(self.data['url']) > 0:
            # create database object
            cit = models.Citation.Citation(self.data['content'], self.data['url'])
            self.session.add(cit)
            response = "Record created successfully"
            
            # commit change to DB
            self.session.commit()
            status = True
        else:
            response = "Content or URL missing"
            status   = False

        return util.ResponseUtils.ResponseUtils.createResponse(status, response, False, self.format)


    def PUT(self, cid):
        """Update an existing citation
        """
        
        # validate
        if len(self.data['content']) > 0 and len(self.data['url']) > 0:
            if len(cid) <= 0:
                response = "Missing parameter (id to be updated)"
                status   = False
            else:
                # create database object
                cit = self.session.query(models.Citation.Citation).filter_by(id=cid).first()
                cit.content = self.data['content']
                cit.url     = self.data['url']
                self.session.add(cit)
                response = "Record updated successfully"

                # commit change to DB                
                self.session.commit()
                status = True
        else:
            response = "Content or URL missing"
            status   = False

        return util.ResponseUtils.ResponseUtils.createResponse(status, response, False, self.format)


    def DELETE(self, cid):
        """Delete an existing citation
        """
        
        # validate
        if len(cid) <= 0:
            response = "Missing parameter (id to be deleted)"
            status   = False
        else:
            # create database object
            cit = self.session.query(models.Citation.Citation).filter_by(id=cid).first()
            self.session.delete(cit)
            
            # commit changes to DB
            self.session.commit()
            status   = True
            response = "Record deleted successfully"

        return util.ResponseUtils.ResponseUtils.createResponse(status, response, False, self.format)

