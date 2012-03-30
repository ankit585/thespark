import web
import re
import uuid
import sys
sys.path.append('../src')

import handler.CitationHandler

urls = ('/citation/(.*)', 'handler.CitationHandler.CitationHandler'
       )


if __name__ == "__main__":
     app = web.application(urls, globals())
     app.run()
