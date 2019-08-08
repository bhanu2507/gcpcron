import logging
import urllib
import urllib2
from google.appengine.api import urlfetch
import webapp2
from lxml import etree
from StringIO import StringIO

class UrlPostHandler(webapp2.RequestHandler):
    """ def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!') """
    """ Demonstrates an HTTP POST form query using urlfetch"""

    form_fields = {
        'searchJob': 'angular'
    }

    def get(self):
        # [START urlfetch-post]
        try:
            form_data = urllib.urlencode(UrlPostHandler.form_fields)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            result = urlfetch.fetch(
                url='https://www.naukri.com/angular-jobs-in-hyderabad',
                payload=form_data,
                method=urlfetch.POST,
                headers=headers)
            parser = etree.HTMLParser() 
            tree   = etree.parse(StringIO(result.content), parser)   
            t = etree.tostring(tree.getroot(),pretty_print=True, method="html") 

            self.response.write(tree.find(".//title").text)
            logging.info(tree.find('.//title').text)
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')  
      

app = webapp2.WSGIApplication([
    ('/', UrlPostHandler),
], debug=True)