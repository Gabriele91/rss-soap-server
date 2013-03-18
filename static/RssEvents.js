/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSEventLogin(nickname,password,fsucces,ffail){
    /**
     * Rss event for login
     */
    RSSSession(
            function(uid){
                RSSLogin(uid,
                    $(nickname).val(),
                    $(password).val(),
                    function (loginevent){
                        if(loginevent){
                            fsucces();
                        }
                        else{
                            ffail();
                        }
                    }
                );
            },
            function(){
                alert("Invalid session [event login]");
            }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSEventIsLogin(fsucces,ffail){
    /**
     * Rss event for Islogin
     */
    RSSSession(
        function(uid){
            RSSIsLogin(uid,
                function (loginevent) {
                    if (loginevent){
                        fsucces();
                    }
                    else{
                        ffail();
                    }
                }
            );
        },
        function(){
            alert("Invalid session [event isLogin]");
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSEventGetId(fsucces,ffail){
    /**
     * Rss event for Islogin
     */
    RSSSession(
        function(uid){
            RSSGetId(uid,
                function (iduser) {
                    if (iduser>-1){
                        fsucces(iduser);
                    }
                    else{
                        ffail();
                    }
                }
            );
        },
        function(){
            alert("Invalid session [event isLogin]");
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSEventLogout(fsucces,ffail){
    /**
     * Rss event for Logout
     */
    RSSSession(
        function(uid){
            RSSLogout(uid,
                function (loginevent) {
                    if (loginevent){
                        fsucces();
                    }
                    else{
                        ffail();
                    }
                }
            );
        },
        function(){
            alert("Invalid session [event logout]");
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSEventAddRss(title,message,fsucces,ffail){
    /**
     * Rss event for AddRss
     */
    RSSSession(
        function(uid){
            RSSAddRss(uid,
                title,
                message,
                function (idret) {
                    if (idret===false){
                        ffail();
                    }
                    else{
                        fsucces(idret);
                    }
                }
            );
        },
        function(){
            alert("Invalid session [event addRss]");
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSEventReadRss(fsucces,ffail){
    /**
     * Rss event for ReadRss
     */
    RSSSession(
        function(uid){
            RSSReadRss(uid,
                function (idret) {
                    if (idret===false){
                        ffail();
                    }
                    else{
                        fsucces(idret);
                    }
                }
            );
        },
        function(){
            alert("Invalid session [event readRss]");
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSEventDeleteRss(rssId,fsucces,ffail){
    /**
     * Rss event for DeleteRss
     */
    RSSSession(
        function(uid){
            RSSDeleteRss(uid,
                rssId,
                function (succesfull) {
                    if (succesfull===false){
                        ffail();
                    }
                    else{
                        fsucces();
                    }
                }
            );
        },
        function(){
          alert("Invalid session [event deleteRss]");
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSEventAddUser(nickname,password,name,surname,email,fsucces,ffail){
    /**
     * Rss event for AddUser
     */
    RSSSession(
        function(uid){
            RSSAddUser(uid,
                nickname,
                password,
                name,
                surname,
                email,
                function (idret) {
                    if (idret=="true"){
                        fsucces();
                    }
                    else{
                        if(idret===false)
                            idret="fail connection";
                        ffail(idret);
                    }
                }  
            );
        },
        function(){
            alert("Invalid session [event readRss]");
        }
    );
}
/**
 * @author Mirco Tracolli
 * @author Gabriele Di Bari
 */
function RSSEventGetMemberInfo(fsucces,ffail){
    /**
     * Rss event for GetMemberInfo
     */
    RSSSession(
        function(uid){
            RSSGetMemberInfo(uid,
                function (arrayRet) {
                    if (arrayRet != false) {
                        fsucces(arrayRet["string"]);
                    }
                    else{
                        ffail();
                    }                              
                }
            );
        },
        function(){
            alert("Invalid session [event GetMemberInfo]");
        }
    );
}
/**
 * @author Mirco Tracolli
 * @author Gabriele Di Bari
 */
function RSSEventEditMemberInfo(nickname,name,surname,email,password,fsucces,ffail){
    /**
     * Rss event for EditMemberInfo
     */
    RSSSession(
        function(uid){
            RSSEditMemberInfo(uid,
                nickname,
                name,
                surname,
                email,
                password,
                function (ret) {
                    console.log(ret);
                    if (ret["string"]["0"]["#text"] != "false") {
                        fsucces();
                    }
                    else{
                        ffail(ret["string"]["1"]["#text"]);
                    }                              
                }
            );
        },
        function(){
            alert("Invalid session [event EditMemberInfo]");
        }
    );
}
/**
 * @author Mirco Tracolli
 * @author Gabriele Di Bari
 */
function RSSEventRssSiteAdd(url,fsucces,ffail){
    /**
     * Rss event for EditMemberInfo
     */
    RSSSession(
        function(uid){
            RSSAddRssSite(uid,
                          url,
                function (ret) {
                    if (ret > 0) {
                        fsucces();
                    }
                    else{
                        ffail(ret);
                    }
                }
            );
        },
        function(){
            alert("Invalid session [event AddRssSite]");
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSEventReadRssFromSite(fsucces,ffail){
    /**
     * Rss event for EditMemberInfo
     */
    RSSSession(
        function(uid){
            RSSReadRssSite(uid,
                function (valueret) {
                    if (valueret===false){
                        ffail();
                    }
                    else{
                        fsucces(valueret);
                    }
                }
            );
        },
        function(){
            alert("Invalid session [event ReadRssSite]");
        }
    );
}
/**
 * @author Gabriele Di Bari
 * @author Mirco Tracolli
 */
function RSSEventDeleteRssSite(idlink,fsucces,ffail){
    /**
     * Rss event for EditMemberInfo
     */
    RSSSession(
        function(uid){
            RSSDeleteRssSite(uid,idlink,
                function (valueret) {
                    if (valueret===false){
                        ffail();
                    }
                    else{
                        fsucces();
                    }
                }
            );
        },
        function(){
            alert("Invalid session [event DeleteRssSite]");
        }
    );
}
