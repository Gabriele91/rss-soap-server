#python lib
import feedparser
import xml
#import Rss lib
from dbConnection import *
from time import mktime
from datetime import datetime

def loggerDebug(argstr):
    sys.stdout.write(argstr+"\n")
    sys.stdout.flush()

class RssSite(object):
    """
    Read an online rss feed
    
    Attributes:
        rss: it will be contain the feedparser module result
        url: the rss url
        validRss: boolean with information of a valid rss feed
    """
    def __init__(self, member):
        """ Initialize onlineRss class
        
        Args:
            url: an rss url
        """
        self.dbcon=DbConnection()
        self.member=member
    
    def addUrl(self, url):
        """ Add an url to RssSite object
        
        Returns:
            Return an integer, -1 in case of fail
        """
        loggerDebug("VALID URL")
        if(self.vaildUrl(url)==False):
            return -1
        #add url
        cr=self.dbcon.cursor()
        squery="INSERT INTO RssSite(link,idmember) VALUES(%s,%s)"
        cr.execute(squery,[url,self.member.id()])
        self.dbcon.commit()
        #return id
        squery="SELECT MAX(id) AS mid FROM RssSite"
        cr.execute(squery)
        ret = cr.fetchone()
        cr.close()
        if ret!=None:
            return int(ret[0])
        return -2
    
    def deleteUrl(self, urlid):
        """ Delete an url from RssSite object
        
        Args:
            urlid : the id of rsslink
        """
        cr=self.dbcon.cursor()        
        squery="DELETE FROM RssSite WHERE id=%s AND idmember=%s "
        cr.execute(squery,[urlid,self.member.id()])
        self.dbcon.commit()
        cr.close()
        return True
        
    def getUrls(self):
        """ Get all urls from RssSite object
        
        Returns:
            An array with id and link
        """
        #return Urls
        cr=self.dbcon.cursor()
        squery="SELECT id,link FROM RssSite WHERE idmember=%s"
        cr.execute(squery,[self.member.id()])
        return cr.fetchall()
    
    
    @staticmethod
    def vaildUrl(url):
        """ Check inf an url is a valid rss
        
        Returns:
            Return True or False depending on whether the rss
            url is validafter
        """
        loggerDebug(url)
        rss = feedparser.parse(url)
        if len(rss.entries) <= 0:
            return False
        return True
    
    def getUrlsValues(self):
        """ Get all urls in the Rss object
        
        Return an array
        """
        urls=self.getUrls()
        values=[]
        for url in urls:
            parseObj=feedparser.parse(url[1])
            entriesObj=parseObj.entries
            values.append([url[0],entriesObj])
        return values
    
    def getEntries(self):
        """Get all rss entries
        
        Returns:
            Return a void array if there's an error
            or an array of array of strings:
            
        """
        values=self.getUrlsValues()
        entries = []
        for rsselements in values:
            for item in rsselements[1]:
                i = []
                i.append(str(rsselements[0]))
                i.append(item.title)
                i.append(item.link)
                i.append(item.description)
                i.append(item.published)
                i.append(item.published_parsed)
                entries.append(i)
        ##
        # Sorted function
        #   Key = published_parsed, converted in deltatime
        #   CMP = subtraction from deltatime
        #   reverse = to have descending order
        #
        # After sorting we convert published_parsed in a string
        # to have a correct serialization from soap
        sortedEntries = sorted(entries,key=lambda i: datetime.fromtimestamp(mktime(i[5])),cmp=lambda x,y: int((x-y).total_seconds()),reverse=True)
        for x in range(0,len(sortedEntries)):
            sortedEntries[x][5] = str(sortedEntries[x][5])
        return sortedEntries


class Rss(object):
    
    def __init__(self,member):
        """ Initialize Rss object
        
        Args :
            member : member object
        """
        self.dbcon=DbConnection()
        self.member=member

    def fields(self):
        """ Get all fields
        """
        cr=self.dbcon.cursor()
        squery="SELECT id,title,message,postdate FROM Rss WHERE idmember=%s ORDER BY postdate DESC"
        cr.execute(squery,[self.member.id()])
        ret = cr.fetchall()
        arrayret=[]
        for row in ret:
            arrayret.append([str(row[0]),row[1],row[2],str(row[3])])
        cr.close()
        return arrayret

    @staticmethod
    def filsdsFromId(mid):
        """ Get all fields by id
        
        Args :
            mid : member id
        """
        dbcon=DbConnection()
        cr=dbcon.cursor()
        squery="SELECT id,title,message,postdate FROM Rss WHERE idmember=%s ORDER BY postdate DESC"
        cr.execute(squery,[mid])
        ret = cr.fetchall()
        arrayret=[]
        for row in ret:
            arrayret.append([str(row[0]),row[1],row[2],str(row[3])])
        cr.close()
        return arrayret

    def insert(self,app,title,message,postdate):
        """ Insert an Rss message
        
        Args :
            app : server app, useful for debugging
            title : Rss title
            message : Rss message
            postdate : Rss insert date
        """
        #insert message
        cr=self.dbcon.cursor()
        squery="INSERT INTO Rss(title,message,postdate,idmember) VALUES(%s,%s,%s,%s)"
        cr.execute(squery,[title,message,postdate,self.member.id()])
        self.dbcon.commit()
        #return id
        squery="SELECT MAX(id) AS mid FROM Rss"
        cr.execute(squery)
        ret = cr.fetchone()
        cr.close()
        if ret!=None:
            return int(ret[0])
        return -1

    def delete(self,idrss):
        """ Delete an Rss message by id
        
        Args:
            idrss : rss id
        """
        cr=self.dbcon.cursor()
        squery="DELETE FROM Rss WHERE id=%s AND idmember=%s "
        cr.execute(squery,[idrss,self.member.id()])
        self.dbcon.commit()
        cr.close()


