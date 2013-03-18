/**
 * From W3S
 * 
 * http://www.w3schools.com/js/js_cookies.asp
 * 
 * setCookie
 * getCookie
 */
function setCookie(c_name,value,exdays){
    var exdate=new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value=escape(value) + ((exdays==null) ? "" : "; expires="+exdate.toUTCString());
    document.cookie=c_name + "=" + c_value;
}
function getCookie(c_name)
{
    var i,x,y,ARRcookies=document.cookie.split(";");
    for (i=0;i<ARRcookies.length;i++){
        x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
        y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
        x=x.replace(/^\s+|\s+$/g,"");
        if (x==c_name){
            return unescape(y);
        }
    }
}
/**
 * Function that convert an xml to json
 * @param {string} xml an xml object string
 * @return {string} obj a json dictionary
 */
function xmlToJson(xml) {
  // Create the return object
  var obj = {};
  if (xml.nodeType == 1) { // element
    // do attributes
    if (xml.attributes.length > 0) {
        obj["@attributes"] = {};
        for (var j = 0; j < xml.attributes.length; j++) {
            var attribute = xml.attributes.item(j);
            obj["@attributes"][attribute.nodeName] = attribute.nodeValue;
        }
    }
  } else if (xml.nodeType == 3) { // text
        obj = xml.nodeValue;
  }
  // do children
  if (xml.hasChildNodes()) {
    for(var i = 0; i < xml.childNodes.length; i++) {
        var item = xml.childNodes.item(i);
        var nodeName = item.nodeName;
        nodeName = nodeName.indexOf(":")>0 ? 
                       nodeName.split(":")[1] :  
                       nodeName;
        if (typeof(obj[nodeName]) == "undefined") {
            obj[nodeName] = xmlToJson(item);
        } else {
            if (typeof(obj[nodeName].push) == "undefined") {
                var old = obj[nodeName];
                obj[nodeName] = [];
                obj[nodeName].push(old);
            }
            obj[nodeName].push(xmlToJson(item));
        }
    }
  }
  return obj;
};
/**
 * @author Mirco Tracolli
 * @author Gabriele Di Bari
 * @fileoverview JQUERY is required
 */
/**
 * site web url
 * old defaultUrl : http://rss-soap-server.herokuapp.com/soap
 */
var defaultUrl = window.location.protocol+"//"+window.location.host+"/soap";
/**
 * fix console object for ie6 to ie9
 */
if(typeof console == 'undefined'){
    this.console={ log:function(){} }
}
/**
 * Class that contain Soap functions
 * @param {string} urlSoapServer the url of the soap web server
 * @constructor
 * @extends {goog.Disposable}
 */
function SoapApi(urlSoapServer) {
    /**
     * Constructor for a singleton
     */
    if ( SoapApi.prototype._singletonInstance ){
        if(!(typeof urlSoapServer === 'undefined' || urlSoapServer==null))
            this.SOAPSERVER = urlSoapServer;
        return SoapApi.prototype._singletonInstance;
    }
    /**
     * first call save object in singleton istance
     */
      SoapApi.prototype._singletonInstance = new objectSoapApi(urlSoapServer);
      return SoapApi.prototype._singletonInstance;
    
    /**
     * An object that can manage soap
     * @param {string} urlSoapServer the url of the soap web server
     */
    function objectSoapApi(urlSoapServer){
          /**
         * if is not def set default url
         */
        if(!(typeof urlSoapServer === 'undefined' || urlSoapServer==null))
            this.SOAPSERVER = urlSoapServer;
        else
            this.SOAPSERVER = defaultUrl
        /**
         * Some constant variables with parameters that will be replaced
         * @constant
         * @type String
         */
        this.METHODE = "  <nsRss:METHOD xmlns:nsRss=\"NAMESPACE\"> \n";
        this.METHODECLOSE = "  </nsRss:METHOD> \n";
        this.ARGE = "   <NAME xsi:type='xsd:TYPE'>VALUE</NAME>\n";
        
        this.createSoapMessage = function (namespace, method, args) {
            /**
             * @param {String} namespace
             * @param {String} method
             * @param {Dict} args { varName : [elementType,elementValue] }
             * @returns {Array} [message, tagResponse]
            */
            var soapMessage = "<?xml version=\"1.0\" encoding=\"utf-8\"?> \n";
            soapMessage += "<SOAP-ENV:Envelope \n";
            soapMessage += "  xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\" \n";
            soapMessage += "  SOAP-ENV:encodindStyle=\"http://schemas.xmlsoap.org/soap/encoding/\" \n"; 
            soapMessage += "  xmlns:SOAP-ENC=\"http://schemas.xmlsoap.org/soap/encoding/\" \n"; 
            soapMessage += "  xmlns:xsi=\"http://www.w3.org/1999/XMLSchema-instance\" \n";
            soapMessage += "> \n";
            soapMessage += " <SOAP-ENV:Body> \n";
            soapMessage += this.METHODE.replace("NAMESPACE",namespace).replace("METHOD",method);
            if (args != null && !(args instanceof Array)) {
                for (var k in args) {
                    soapMessage += this.ARGE.replace(/\bNAME\b/gi,k).replace("TYPE",args[k][0]).replace("VALUE",args[k][1]);
                }
            }
            soapMessage += this.METHODECLOSE.replace("METHOD",method);
            soapMessage += " </SOAP-ENV:Body> \n"; 
            soapMessage += "</SOAP-ENV:Envelope>";
            return [soapMessage,String(method+"Response"),String(method+"Result")];
        };
        
        this.sendMessage = function (message,callback,callbackfail) {
            $.post(this.SOAPSERVER, message[0],
                function(data, textStatus, jqXHR) {/* succes */},"xml"
            ).fail(function(data) {
                callbackfail();
            }).done(function(data) {
                /* alert("Done"); */
                var parsedData = xmlToJson(data);
                console.log(JSON.stringify(parsedData));
				if ("Fault" in parsedData["Envelope"]["Body"]) {
					callbackfail();					
				}
                callback(parsedData["Envelope"]["Body"][message[1]][message[2]]);
            }).error(function(XMLHttpRequest, textStatus, errorThrown) { 
                alert("There are some errors: " + textStatus + "\n -> " + errorThrown);
				callbackfail();				
            });
        }
    }
    
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 * @fileoverview manage an Rss session
 */
function RSSSession(callbackidsession,callbackidsessionfail){
    /**
     * Function that manage Rss session
     * @param {Function} callbackidsession function to use if session is valid
     * @param {Function} callbackidsessionfail function to use if session is not valid
     */
    sessioneid=getCookie("RSSSession");
    if(sessioneid!=null && sessioneid!=""){
        soap=SoapApi();
        soapMessage=soap.createSoapMessage("rssNS","isValidSession",{"idsession":["string",sessioneid]});
        soap.sendMessage(soapMessage,
            function (res){
                if(res["#text"]=="true"){
                    callbackidsession(sessioneid);
                }
                else {
                    setCookie("RSSSession","",-1);
                    RSSSession(callbackidsession,callbackidsessionfail);
                }
            },
			function(){
				callbackidsessionfail();
				window.location.replace(window.location.protocol+"//"+window.location.host);
				}
        );
    }
    else{
        /**
         * call soap rss service and get session ID
         */
        soap=SoapApi();
        soapMessage=soap.createSoapMessage("rssNS","getSession",{"idsession":["string","none"]});
        soap.sendMessage(soapMessage,
            function (res){
                sessioneid=res["#text"];
                setCookie("RSSSession",sessioneid,30);
                callbackidsession(sessioneid);
            },
			function(){
				callbackidsessionfail();
				window.location.replace(window.location.protocol+"//"+window.location.host);
				}
        );
    }
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSLogin(sessionid,nickname,password,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","login",
        {
            "idsession":["string",sessionid],
            "nickname":["string",nickname],
            "password":["string",password]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
            funEndReq(res["#text"]=="true");
        },
        function(){
            funEndReq(false);
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSIsLogin(sessionid,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","isLogged",
        {
            "idsession":["string",sessionid]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
            funEndReq(res["#text"]=="true");
        },
        function(){
            funEndReq(false);
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSGetId(sessionid,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","getId",
        {
            "idsession":["string",sessionid]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
            funEndReq(parseInt(res["#text"]));
        },
        function(){
            funEndReq(false);
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSLogout(sessionid,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","logout",
        {
            "idsession":["string",sessionid]
        });
    soap.sendMessage(soapMessage,
        function (res){
            funEndReq(res["#text"]=="true");
        },
        function(){
           funEndReq(false);
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSAddRss(sessionid,title,message,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","addRss",
        {
            "idsession":["string",sessionid],
            "title":["string",title],
            "message":["string",message]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
			funEndReq(parseInt(res["#text"]));
        },
        function(){
            funEndReq(false);
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSReadRss(sessionid,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","returnListRss",
        {
            "idsession":["string",sessionid]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
            funEndReq(res);
        },
        function(){
            funEndReq(false);
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSDeleteRss(sessionid, rssId,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","removeRss",
        {
            "idsession":["string",sessionid],
            "rssId":["integer",rssId]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
            funEndReq(res);
        },
        function(){
            funEndReq(false);
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSAddUser(sessionid,nickname,password,name,surname,email,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","addUser",
        {
        "idsession":["string",sessionid],
        "nickname":["string",nickname],
        "password":["string",password],
        "name":["string",name],
        "surname":["string",surname],
        "email":["string",email]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
            funEndReq(res["#text"]);
        },
        function(){
            funEndReq(false);
        }
    );
}
/**
 * @author Mirco Tracolli
 * @author Gabriele Di Bari
 */
function RSSGetMemberInfo(sessionid,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","getMemberInfo",
        {
            "idsession":["string",sessionid]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
            funEndReq(res);
        },
        function(){
            funEndReq(false);
        }
    );
}
/**
 * @author Mirco Tracolli
 * @author Gabriele Di Bari
 */
function RSSEditMemberInfo(sessionid,nickname,name,surname,email,password,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","editMember",
        {
            "idsession":["string",sessionid],
            "nickname":["string",nickname],
            "name":["string",name],
            "surname":["string",surname],
            "email":["string",email],
            "password":["string",password]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
            funEndReq(res);
        },
        function(){
            funEndReq(false);
        }
    );
}
/**
 * @author Mirco Tracolli
 * @author Gabriele Di Bari
 */
function RSSAddRssSite(sessionid,url,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","addLinkRss",
        {
            "idsession":["string",sessionid],
            "link":["string",url]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
			funEndReq(parseInt(res["#text"]));
        },
        function(){
            funEndReq(false);
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSReadRssSite(sessionid,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","getRssFromUrls",
        {
            "idsession":["string",sessionid]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
            funEndReq(res);
        },
        function(){
            funEndReq(false);
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSDeleteRssSite(sessionid,rsslinkid,funEndReq){
    /**
     * call soap rss service and get session ID
     */
    soap=SoapApi();
    soapMessage=soap.createSoapMessage("rssNS","removeLinkRss",
        {
            "idsession":["string",sessionid],
            "idurl":["integer",rsslinkid]
        }
    );
    soap.sendMessage(soapMessage,
        function (res){
            funEndReq();
        },
        function(){
            funEndReq(false);
        }
    );
}