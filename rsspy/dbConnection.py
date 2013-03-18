#python lib
import os, sys, inspect
#psycopg2 lib
import psycopg2


def loggerDebug(argstr):
    sys.stdout.write(argstr+"\n")
    sys.stdout.flush()

def singleton(class_):
    """ Decorator function for singleton classes
    """
    _slInstances = {}
    def getinstance(*args, **kwargs):
        if class_ not in _slInstances:
            _slInstances[class_] = class_(*args, **kwargs)
        return _slInstances[class_]
    return getinstance

@singleton
class DbConnection(object):
    """Database Connection Class
    
    The database connection is a singleton,
    so there will be only one istance of this class
    
    Attributes:
        strconf : string that will contain configuration
            file items
        conn : connection with postgresql database
    """
    def __init__(self):
        """ Initialization of DbConnection
        
        It will create the database connection
        """
        self.strconf=""
        dirfile=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        with open(dirfile+"/config.db") as fl:
            for line in fl.readlines():
                self.strconf+=" "+line                
        self.conn = psycopg2.connect(self.strconf)

    def cursor(self):
        """ Method to get a cursor from database connection
        
        Returns:
            cursor object
        """
        return self.conn.cursor()
    
    def commit(self):
        """ Method to apply the changes to the database
        """
        self.conn.commit()
    
    def closeIstance(self):
        """ Method that will close the database connection
        """
        self.conn.close()
        
    
    

