import logging
import urllib
import urllib2
from google.appengine.api import urlfetch
import webapp2
from lxml import etree
from StringIO import StringIO
import os
import MySQLdb

CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

def connect_to_cloudsql():
    # When deployed to App Engine, the `SERVER_SOFTWARE` environment variable
    # will be set to 'Google App Engine/version'.
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # Connect using the unix socket located at
        # /cloudsql/cloudsql-connection-name.
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)

        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd=CLOUDSQL_PASSWORD)

    # If the unix socket is unavailable, then try to connect using TCP. This
    # will work if you're running a local MySQL server or using the Cloud SQL
    # proxy, for example:
    #
    #   $ cloud_sql_proxy -instances=your-connection-name=tcp:3306
    #
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd=CLOUDSQL_PASSWORD)

    return db

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
                db = connect_to_cloudsql()
                cursor = db.cursor()
                cursor.execute("INSERT INTO `cityjobs`.`jobtrack`(`tech`, `city`, `logdate`, `count`) VALUES ('" + "angular" +"', '" + "hyderabad" +"', '" + "2019-08-09" + "', '" + tree.find('.//title').text.split("-")[1].split(" ")[1].strip() + "');")
                db.commit()
                cursor.close()
                db.close()
            else:
                self.response.status_code = result.status_code
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
        # [END urlfetch-get] 
      

app = webapp2.WSGIApplication([
    ('/', UrlPostHandler),
], debug=True)