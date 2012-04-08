import models.Citation
import util.DBUtils
import util.ResponseUtils
import json
import web

class CitationHandler():

    def GET(self, cid):
        """Display a single citation or full list if no ID specified
        """
        session = util.DBUtils.DBUtils.getSession()
        cits = None
        
        # get format from url parameters
        url_params  = web.input(format='')
        format = url_params.format
        
        if len(cid) <= 0:
            cits = session.query(models.Citation.Citation).order_by(models.Citation.Citation.id).all()
        else:
            cits = session.query(models.Citation.Citation).filter_by(id=cid).all()

        return util.ResponseUtils.ResponseUtils.createResponse(True, cits, True, format)



    def POST(self, uselessvar):
        """Create a new citation
            uselessvar is simply a placeholder
        """
        
        # get and parse raw post data
        data = (web.data())
        data = dict([part.split('=') for part in data.split('&')])

        # create database session
        session = util.DBUtils.DBUtils.getSession()
    
        # validate
        if len(data['content']) > 0 and len(data['url']) > 0:
            # create database object
            cit = models.Citation.Citation(data['content'],data['url'])
            session.add(cit)
            response = "Record created successfully"
            
            # commit change to DB
            session.commit()
            status = True
        else:
            response = "Content or URL missing"
            status   = False

        return util.ResponseUtils.ResponseUtils.createResponse(status, response, False)


    def PUT(self, cid):
        """Update an existing citation
        """
        
        # get and parse raw post data
        data = (web.data())
        data = dict([part.split('=') for part in data.split('&')])

        # create database session
        session = util.DBUtils.DBUtils.getSession()

        # validate
        if len(data['content']) > 0 and len(data['url']) > 0:
            if len(cid) <= 0:
                response = "Missing parameter (id to be updated)"
                status   = False
            else:
                # create database object
                cit = session.query(models.Citation.Citation).filter_by(id=cid).first()
                cit.content = data['content']
                cit.url     = data['url']
                session.add(cit)
                response = "Record updated successfully"

                # commit change to DB                
                session.commit()
                status = True
        else:
            response = "Content or URL missing"
            status   = False

        return util.ResponseUtils.ResponseUtils.createResponse(status, response, False)


    def DELETE(self, cid):
        """Delete an existing citation
        """
        
        # create database session
        session = util.DBUtils.DBUtils.getSession()

        # validate
        if len(cid) <= 0:
            response = "Missing parameter (id to be deleted)"
            status   = False
        else:
            # create database object
            cit = session.query(models.Citation.Citation).filter_by(id=cid).first()
            session.delete(cit)
            
            # commit changes to DB
            session.commit()
            status   = True
            response = "Record deleted successfully"

        return util.ResponseUtils.ResponseUtils.createResponse(status, response, False)

