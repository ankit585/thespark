import models.Citation
import util.DBUtils
import util.ResponseUtils
import json
import web

class CitationHandler():

  def GET(self,cid):
    session = util.DBUtils.DBUtils.getSession()
    cits = None
    if len(cid) <= 0:
       cits = session.query(models.Citation.Citation).order_by(models.Citation.Citation.id).all()
    else:
       cits = session.query(models.Citation.Citation).filter_by(id=cid).all()

    return util.ResponseUtils.ResponseUtils.createResponse(True,cits,True)



  def POST(self,cid):
    data = (web.data())
    data = dict([part.split('=') for part in data.split('&')])

    session = util.DBUtils.DBUtils.getSession()
    response = ""
    if len(data['content']) > 0 and len(data['url']) >0:

       if len(cid) <= 0:
         cit = models.Citation.Citation(data['content'],data['url'])
         session.add(cit)
         response = "Record created successfully"
       else:
         cit = session.query(models.Citation.Citation).filter_by(id=cid).first()
         cit.content = data['content']
         cit.url     = data['url']
         session.add(cit)
         response = "Record updated successfully"
       session.commit()
       status   = True
    else:
       response = "Content or URL missing"
       status   = False

    return util.ResponseUtils.ResponseUtils.createResponse(status,response,False)


  def PUT(self,cid):
    data = (web.data())
    data = dict([part.split('=') for part in data.split('&')])

    session = util.DBUtils.DBUtils.getSession()
    response = ""
    if len(data['content']) > 0 and len(data['url']) >0:

       if len(cid) <= 0:
         response = "Record does not exist"
         status   = False
       else:
         cit = session.query(models.Citation.Citation).filter_by(id=cid).first()
         cit.content = data['content']
         cit.url     = data['url']
         session.add(cit)
         session.commit()
         status   = True
         response = "Record updated successfully"
    else:
       response = "Content or URL missing"
       status   = False

    return util.ResponseUtils.ResponseUtils.createResponse(status,response,False)

  def DELETE(self,cid):

      session = util.DBUtils.DBUtils.getSession()
      response = ""
      if len(cid) <= 0:
         response = "Missing parameter (id to be deleted)"
         status   = False
      else:
         cit = session.query(models.Citation.Citation).filter_by(id=cid).first()
         session.delete(cit)
         session.commit()
         status   = True
         response = "Record deleted successfully"

      return util.ResponseUtils.ResponseUtils.createResponse(status,response,False)

