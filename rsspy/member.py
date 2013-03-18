#python lib
import threading
import thread
import io
import os, sys, re
from time import time, sleep
#import Rss lib
from dbConnection import *
from rss import *

# Regular expression to check inputs
checkEmail = lambda s : re.search("^[^\.]([\w]*[\-]{0,1}[\w]*|[\w]*[\.]{0,1}[\w]*)*\@([\w]+[\-]{0,1}[\w]*|[\w]+[\.]{0,1}[\w]*)+(\.)+[\w]+$", s)
checkNickname = lambda s : re.search("^[^0-9][\w]+$", s)
checkName = lambda s : re.search("^[a-zA-Z]+$", s)
checkSurname = lambda s : re.search("^[a-zA-Z]+$", s)
checkPasswd = lambda s : re.search("^((\w\-\']|\s)*(\.?(\s|[\w\-\']|$))?)+$", s)

def loggerDebug(argstr):
    sys.stdout.write(argstr+"\n")
    sys.stdout.flush()


class Member(object):
    """ Class for site member
    
    Objects of this class will represent the site users
    
    Attributes:
        dbcon : connection to database
        _mid : user id
        _login : boolean for login session
        _name : user name
        _surname : user surname
        _nickname : user nickname
        _email : user email
        _rss : RSS object
    """
    def __init__(self):
        """ Initialization of Member
        """
        self.dbcon=DbConnection()
        self._mid=-1
        self._login=False
        self._name=""
        self._surname=""
        self._nickname=""
        self._email=""
        self._rss=Rss(self)
        self._rsssite=RssSite(self)
        
    def _editValue(self,namevalue,value):
        """ Function to edit a member attribute
        """
        cr=self.dbcon.cursor()
        squery="UPDATE Member SET "+namevalue+"=%s WHERE id=%s"
        cr.execute(squery,[value,self._mid])
    
    def login(self,nickname,password):
        """ Function to login with a member
        """
        cr=self.dbcon.cursor()
        squery= """
                SELECT id,name,surname,email 
                FROM Member 
                WHERE 
                nickname=%s AND password=md5(%s)
                """
        cr.execute(squery,[nickname,password])        
        ret = cr.fetchone()
        if ret != None :
            self._mid,self._name,self._surname,self._email = ret
            self._login=True
            self._nickname=nickname
        cr.close()
    
    def getRssSite(self):
        return self._rsssite
    
    
    def getRss(self):
        """ Function to get all Rss of a member
        """
        return self._rss

    def islogin(self):
        """ Function to check if a member is logged
        """
        return self._login
    
    def logout(self):
        """ Function to logoun with a member
        """
        self._mid=-1
        self._login=False
        self._name=""
        self._surname=""
        self._nickname=""
        self._email=""
    
    def editPassword(self,password):
        """ Function to edit the member password
        """
        cr=self.dbcon.cursor()
        squery="UPDATE Member SET password=md5(%s) WHERE id=%s"
        cr.execute(squery,[password,self._mid])
        cr.close()
    
    def id(self):
        """ Function to get member id
        """
        return self._mid
    
    def nickname(self,nickname=None):
        """ Function to get member nickname
        """
        if nickname!=None:
            cr=self.dbcon.cursor()
            squery= """
                    SELECT nickname
                    FROM Member 
                    WHERE 
                    nickname=%s
                    """
            cr.execute(squery,[nickname])        
            ret = cr.fetchone()
            if ret == None :
                self._editValue("nickname",nickname)
                self._nickname=nickname
            else:
                return False
        return self._nickname
    
    def name(self,vname=None):
        """ Function to get member name
        """
        if vname!=None:
            self._editValue("name",vname)
            self._name=vname
        return self._name
    
    def surname(self,vsurname=None):
        """ Function to get member surname
        """
        if vsurname!=None:
            self._editValue("surname",vsurname)
            self._surname=vsurname
        return self._surname
    
    def email(self,vemail=None):
        """ Function to get member email
        """
        if vemail!=None:
            self._editValue("surname",vemail)
            self._email=vemail
        return self._email
    
    def editUser(self, nickname, name, surname, email, password):
        ret = {}
        null = 0
        
        if len(name) != 0:
            if checkName(name) is not None:
                if name == self._name:
                    ret["name"] = True
                else:
                    ret["name"] = self.name(name)
            else:
                ret["name"] = False
        else:
            null += 1
        if len(surname) != 0:
            if checkSurname(surname) is not None:
                if surname == self._surname:
                    ret["surname"] = True
                else:
                    ret["surname"] = self.surname(surname)
            else:
                ret["surname"] = False
        else:
            null += 1
        if len(nickname) != 0:
            if checkNickname(nickname) is not None:
                if nickname == self._nickname:
                    ret["nickname"] = True
                else:
                    ret["nickname"] = self.nickname(nickname)
            else:
                ret["nickname"] = False
        else:
            null += 1
        if len(password) != 0:
            if checkPasswd(password) is not None:
                ret["password"] = self.editPassword(password)
            else:
                ret["password"] = False
        else:
            null += 1
        if len(email) != 0:
            if checkEmail(email) is not None:
                if email == self._email:
                    ret["email"] = True
                else:
                    ret["email"] = self.email(email)
            else:
                ret["email"] = False
        else:
            null += 1
        
        error = ""
        ok = ""
        for k,v in ret.items():
            if v == False:
                error += str(k)+","
            else:
                ok += str(k)+","
        
        if error!= "":
            if ok != "":
                error = error[:-1]+" \nAppropriate variables changed: "+ok[:-1]
            else:
                error = error[:-1]
            return ("false",error)
        
        if null == 5:
            return ("false","empty form!")
        return ("true","Insert completed")
    
    def createUser(self, name, surname, nickname, password, email):
        """ Function to create an user
        
        Args:
            name : string
            surname : string
            nickname : string
            password : string
            email : string
        Returns:
            True or False based on the user's insertion
        """
        if checkName(name) is None:
            return (False,"Unaccepted name")
        if checkSurname(surname) is None:
            return (False,"Unaccepted surname")
        if checkNickname(nickname) is None:
            return (False,"Unaccepted nickname")
        if checkPasswd(password) is None:
            return (False,"Unaccepted password")
        if checkEmail(email) is None:
            return (False,"Unaccepted email")
        
        #nickname?
        loggerDebug("#nickname?")
        cr=self.dbcon.cursor()
        squery= """
                SELECT * FROM Member WHERE lower(nickname)=lower(%s) 
                """
        cr.execute(squery,[nickname])
        if cr.fetchone()!=None:
            cr.close()
            return (False,"nickname already exist")
        #email?
        loggerDebug("#email?")
        squery= """
                SELECT * FROM Member WHERE lower(email)=lower(%s) 
                """
        cr.execute(squery,[email])
        if cr.fetchone()!=None:
            cr.close()
            return (False,"email already exist")
        #insert member       
        loggerDebug("#insert member") 
        squery="""
               INSERT INTO Member(name, surname, nickname, password, email) 
               VALUES(%s,%s,%s,md5(%s),%s)
               """
        loggerDebug(squery%(name, surname, nickname, password, email))
        cr.execute(squery,[name, surname, nickname, password, email])
        self.dbcon.commit()
        cr.close()
        return True
    


class MembersPool(threading.Thread):
    """ Class for site members pool
    
    The object of this class will contain all the site users
    and will manage the user session. Normaly pool is executed
    in a separate thread.
    
    Attributes:
        pool : dictionary with users
        session_lifetime : max time of a session
        sleep_time : sleep time for the garbage collector
        running : boolean for main loop
        
    """
    def __init__(self, lifetime, sleeptime):
        """ Initialization of pool
        """
        self.pool = {}
        self.session_lifetime = float(lifetime)
        self.sleep_time = sleeptime
        self.running=True
        super(MembersPool, self).__init__()
    
    def close(self):
        """ Delete of pool
        """
        self.running = False
        # I want to kill you!!!
        #thread.exit()
        

    def _makeMember(self, idM):
        """ Add a member to the pool
        """
        member = Member()
        self.pool[idM] = [time(),member]
        return member
    
    def len():
        """ Return the number of members in the pool
        """
        return len(self.pool)

    def pop(idM):
        """ Delete a member from the pool
        """
        self.pool.pop(k)

    def get(self, idM):
        """ Get a member instance if exist or create one
        and return it
        """
        if self.exist(idM):
            return self.pool[idM][1]
        return self._makeMember(idM)
    
    def exist(self, idM):
        """ Check if a member exist
        """
        if idM in self.pool.keys():
            #reset timer
            self.pool[idM][0]=time()
            #exist
            return True
        #not exist
        return False
    
    def run(self):
        """ Main loop of pool thread
        """
        while self.running:
            sleep(self.sleep_time)
            delete_item = []
            for k,v in self.pool.items():
                if (time() - v[0]) > self.session_lifetime:
                    delete_item.append(k)
            for k in delete_item:
                self.pool.pop(k)
        #thread.exit()

