import logging
import urllib
import urllib2
from google.appengine.api import urlfetch
import webapp2
from lxml import etree
from StringIO import StringIO

class UrlPostHandler(webapp2.RequestHandler):
    def get(self):
        # [START urlfetch-get]
        try:
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            result = urlfetch.fetch(
                url='https://www.naukri.com/angular-jobs-in-hyderabad',
                method=urlfetch.POST,
                headers=headers)
            parser = etree.HTMLParser() 
            tree   = etree.parse(StringIO(result.content), parser)      
            if result.status_code == 200:
                self.response.write(result.content)
                logging.info(tree.find('.//title').text.split("-")[1].split(" ")[1].strip())
            else:
                self.response.status_code = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
        # [END urlfetch-get] 
      

app = webapp2.WSGIApplication([
    ('/', UrlPostHandler),
], debug=True)