#python lib
import random
import os
from time import time
#flask lib
from flaskext.enterprise import Enterprise
from flask import Flask, render_template, request, url_for

#config Flask
app = Flask(__name__)

#config Flask Enterprise
enterprise = Enterprise(app)
String = enterprise._sp.String
Integer = enterprise._sp.Integer
Boolean = enterprise._sp.Boolean
AnyAsDict = enterprise._sp.AnyAsDict
Array = enterprise._scls.Array

#config RSS server lib
random.seed(time())



class Service(enterprise.SOAPService):
    """Soap Service Class
    
    Attributes:
        __soap_target_namespace__ : namespace for soap service
        __soap_server_address__ : address of soap service
    """
    __soap_target_namespace__ = 'MyNS'
    __soap_server_address__ = '/soap'

    @enterprise.soap(String, _returns=String)
    def echo(self, mystring):
        """Login with a Soap Member
        
        Args:
            idsession : session identifier
            nickname : username
            password : user's password
        Returns:
            return a boolean
        """
        return mystring
    
    @enterprise.soap(Integer, Integer, _returns=Integer)
    def sum(self, x, y):
        """Login with a Soap Member
        
        Args:
            idsession : session identifier
            nickname : username
            password : user's password
        Returns:
            return a boolean
        """
        return x+y
    
    @enterprise.soap(Integer, Integer, _returns=Boolean)
    def equal(self, x, y):
        """Login with a Soap Member
        
        Args:
            idsession : session identifier
            nickname : username
            password : user's password
        Returns:
            return a boolean
        """
        return x==y


@app.route('/')
def pageIndex():
    """ The index page
    """
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    """ Error 404
    """
    return render_template("404.html"), 404

@app.errorhandler(403)
def forbidden(e):
    """ Error 403
    """
    return render_template("403.html"), 403

@app.errorhandler(410)
def gone(e):
    """ Error 410
    """
    return render_template("410.html"), 410

@app.errorhandler(500)
def internal_server_error(e):
    """ Error 500
    """
    return render_template("500.html"), 500

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
