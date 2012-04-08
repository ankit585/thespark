import web
import re
import uuid
import sys

# go up a level so we can import stuff
sys.path.append('../../src')
# import all the handler modules
import handler.CitationHandler
#import handler.SummationHandler

urls = ('/citation/(.*)', 'handler.CitationHandler.CitationHandler'
       )


if __name__ == "__main__":
     app = web.application(urls, globals())
     app.run()