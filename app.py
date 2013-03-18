#site lib
import rsspy
#python lib
import md5
import random
import os, sys, signal
import atexit
from time import time
from time import strftime
from datetime import timedelta,datetime
#flask lib
from flaskext.enterprise import Enterprise
from flask import Flask, render_template, request, url_for

#config Flask
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=5)
#app.config['SECRET_KEY'] = "develop"

#config Flask Enterprise
enterprise = Enterprise(app)
String = enterprise._sp.String
Integer = enterprise._sp.Integer
Boolean = enterprise._sp.Boolean
Dictionary = enterprise._sp.AnyAsDict
Array = enterprise._scls.Array

#config RSS server lib
random.seed(time())
global POOL
POOL = rsspy.MembersPool(300,180)



class Service(enterprise.SOAPService):
    """Soap Service Class
    
    Attributes:
        __soap_target_namespace__ : namespace for soap service
        __soap_server_address__ : address of soap service
    """
    __soap_target_namespace__ = 'rssNS'
    __soap_server_address__ = '/soap'

    @enterprise.soap(String,_returns=String)
    def getSession(self, idsession):
        """Create a Soap session
        
        Function necessary to the management of the session, in
        particular at the beginning.
        
        Args:
            idsession: actual client session identifier, a string
                of 32 char (md5)
            
        Returns:
            return a string with a valid identifier for the client
            session, for example this is the response without soap
            xml headers:
        """
        # App Debug
        app.logger.debug("getSession")
        if len(idsession)==32 and POOL.exist(idsession) :
            app.logger.debug("exist")
            return idsession
        else:
            # App Debug
            app.logger.debug("not exist")
            #make new id
            newuid=""
            numberid=random.randint(0,1000000000)
            while True:
                newuid=str(md5.new(str(numberid)).hexdigest())
                if not POOL.exist(newuid):
                    break
                numberid+=1
            #make session
            app.logger.debug("newuid:"+newuid)
            POOL.get(newuid)
            #send session id
            app.logger.debug("return newuid")
            return newuid

    @enterprise.soap(String,_returns=Boolean)
    def isValidSession(self,idsession):
        """Check if Soap session is valid
        
        Args:
            idsession : session identifier
            
        Returns:
            return a boolean
        """
        # App Debug
        app.logger.debug("isValidSession call")
        if len(idsession)==32 and POOL.exist(idsession) :
            return True
        return False

    @enterprise.soap(String, String, String, _returns=Boolean)
    def login(self, idsession, nickname, password):
        """Login with a Soap Member
        
        Args:
            idsession : session identifier
            nickname : username
            password : user's password
        Returns:
            return a boolean
        """
        # App Debug
        app.logger.debug("login")
        #get if a valid session
        if self.isValidSession(idsession) :
            #get user  
            user=POOL.get(idsession)
            #execute login
            user.login(nickname,password)
            #get if faild
            return user.islogin()
        return False

    @enterprise.soap(String,_returns=Integer)
    def getId(self,idsession):
        """Return Member id
        
        Args:
            idsession : session identifier
            
        Returns:
            return an integer
        """
        # App Debug
        app.logger.debug("getId")
        if POOL.exist(idsession):
            return POOL.get(idsession).id()
        return -1

    @enterprise.soap(String,_returns=Boolean)
    def isLogged(self,idsession):
        """Check if Soap Member is logged in
        
        Args:
            idsession : session identifier
            
        Returns:
            return a boolean
        """
        # App Debug
        app.logger.debug("isLogged")
        if POOL.exist(idsession):
            return POOL.get(idsession).islogin()
        return False

    @enterprise.soap(String,_returns=Boolean)
    def logout(self,idsession):
        """Logout with a Soap Member
        
        Args:
            idsession : session identifier
            
        Returns:
            return a boolean
        """
        # App Debug
        app.logger.debug("logout")
        if POOL.exist(idsession):
            POOL.get(idsession).logout()
        return True

    @enterprise.soap(String, String, String, String, String, String, _returns=Array(String))
    def editMember(self, idsession, nickname, name, surname, email, password):
        """Edit Soap Member attributes
        
        Args:
            idsession : session identifier
            nickname : new username
            name : user's new name
            surname : user's new surname
            email : user's new email
            password : user's new password
        Returns:
            return an array of strings
        """
        if POOL.exist(idsession):
            return POOL.get(idsession).editUser(nickname, name, surname, email, password)
        return ("false","idsession not exist")
    
    @enterprise.soap(String, _returns=Array(String))
    def getMemberInfo(self, idsession):
        """Get all Soap Member attributes
        
        Args:
            idsession : session identifier
            
        Returns:
            return an array of strings
        """
        attributes = []
        if POOL.exist(idsession):
            attributes.append(POOL.get(idsession).nickname())
            attributes.append(POOL.get(idsession).name())
            attributes.append(POOL.get(idsession).surname())
            attributes.append(POOL.get(idsession).email())
        return attributes

    @enterprise.soap(String,String, String, String, String, String, _returns=String)
    def addUser(self, idsession,name, surname, nickname, password, email):
        """Add a new Soap Member
        
        Args:
            idsession : session identifier
            nickname : username
            name : user's name
            surname : user's surname
            email : user's email
            password : user's password
            
        Returns:
            return a string
        """
        if POOL.exist(idsession):
            # App Debug
            app.logger.debug("addUser")
            if len(name.replace(' ',''))==0: return "invalid name" 
            if len(surname.replace(' ',''))==0: return "invalid surname" 
            if len(nickname.replace(' ',''))==0: return "invalid nickname" 
            if len(password.replace(' ',''))==0: return "invalid password" 
            if len(email.replace(' ',''))==0: return "invalid email"
            # App Debug
            app.logger.debug("send values")
            ret=POOL.get(idsession).createUser(name, surname, nickname, password, email)
            # App Debug
            app.logger.debug("value return:"+str(ret))
            if ret!=True:
                return ret[1]
            return "true"
        return "invalid session"
    
    @enterprise.soap(String, String, String, _returns=Integer)
    def addRss(self, idsession,title, message):
        """Add an RSS
        
        Args:
            idsession : session identifier
            title : rss's message title
            message : rss's message
            
        Returns:
            return an integer
        """
        # App Debug
        app.logger.debug("addRss")
        if POOL.exist(idsession):
            return POOL.get(idsession).getRss().insert(app,title,message,strftime('%Y-%m-%d %H:%M:%S'))
        return 1
    
    @enterprise.soap(String,Integer, _returns=Boolean)
    def removeRss(self, idsession,rssId):
        """Delete an RSS
        
        Args:
            idsession : session identifier
            
        Returns:
            return a boolean
        """
        if POOL.exist(idsession):
            return POOL.get(idsession).getRss().delete(rssId)
        return True
    
    @enterprise.soap(String,_returns=Array(Array(String)))
    def returnListRss(self,idsession):
        """Get all RSSs
        
        Args:
            idsession : session identifier
            
        Returns:
            return an array of arrays of strings
        """
        # App Debug
        app.logger.debug("returnListRss")
        if POOL.exist(idsession):
            arr=POOL.get(idsession).getRss().fields()
            app.logger.debug(str(arr))
            return arr
        return [['']]
    
    @enterprise.soap(String,String,_returns=Integer)
    def addLinkRss(self, idsession, link):
        """Add an RSS site url
        
        Args:
            idsession : session identifier
            link : the rss url
            
        Returns:
            return an integer
        """
        #
        app.logger.debug("addLinkRss "+str(link))
        #
        if POOL.exist(idsession):
            return POOL.get(idsession).getRssSite().addUrl(link)
        return -1
    
    @enterprise.soap(String,Integer,_returns=Boolean)
    def removeLinkRss(self, idsession,idurl):
        """Remove an RSS url
        
        Args:
            idsession : session identifier
            idurl : identifier for rss url
            
        Returns:
            return a boolean
        """
        #
        app.logger.debug("removeLinkRss")
        #
        if POOL.exist(idsession):
            return POOL.get(idsession).getRssSite().deleteUrl(idurl)
        return False
    
    @enterprise.soap(String,_returns=Array(Array(String)))
    def getRssFromUrls(self,idsession):
        """Get all RSS entries
        
        Args:
            idsession : session identifier
            
        Returns:
            return an array of arrays of strings
        """
        #
        app.logger.debug("getRssFromUrls")
        #
        if POOL.exist(idsession):
            return POOL.get(idsession).getRssSite().getEntries()
        return [[""]]

@app.route('/')
def pageIndex():
    """ The index page
    """
    return render_template("index.html")

@app.route('/rss',methods=['GET'])
def memberRss():
    """ Get member RSSs
    """
    searchword = request.args.get('id')
    if searchword is None:
        return page_not_found("rss")
    listRss=rsspy.Rss.filsdsFromId(int(searchword))
    if listRss != None:
        strOut="<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
        strOut+="<rss version=\"2.0\" " 
        strOut+="xmlns:dc=\"http://purl.org/dc/elements/1.1/\" "
        strOut+="xmlns:sy=\"http://purl.org/rss/1.0/modules/syndication/\" "
        strOut+="xmlns:admin=\"http://webns.net/mvcb/\" "
        strOut+="xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" "
        strOut+="xmlns:content=\"http://purl.org/rss/1.0/modules/content/\">\n"
        strOut+="<channel>\n"
        for rss in listRss:
            strOut+="<item>\n"
            strOut+="<title>"+rss[1]+"</title>\n"
            strOut+="<link>"+request.url+"</link>\n"
            strOut+="<description>"+rss[2]+"</description>\n"
            dtpy=datetime.strptime(rss[3],"%Y-%m-%d %H:%M:%S")
            strOut+="<pubDate>"+dtpy.strftime('%a, %d %b %Y %H:%M:%S')+"</pubDate>\n"
            strOut+="</item>\n"
        strOut+="</channel></rss>\n"
        return strOut

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

def closeApp():
    """ Close whole application function
    """
    #get POOL
    global POOL
    #stop thread
    POOL.close()
    if POOL.isAlive():
        POOL.join()

def closeConnection():
    """ Close connection function
    """
    #close connection
    dbcon=rsspy.DbConnection()
    dbcon.closeIstance()

def ctrlC_handler(signal, frame):
    """ Handler for Ctrl+C event
    """
    closeApp()
    sys.exit(0)


if __name__ == '__main__':
    #register signal
    signal.signal(signal.SIGINT, ctrlC_handler)
    #register closer method
    atexit.register(closeConnection)
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
