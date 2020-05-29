var userAgent = navigator.userAgent;
    var host = window.location.hostname;
    var pathn = window.location.pathname;
    var isNewUser = "";
    var user_id = findCookieUserId(document.cookie);
    if (user_id == null) {
        user_id = uuidv4();
        isNewUser = true;
        document.cookie = "user_id="+user_id;
    }
    var url = new URL('http://'+ window.location.host + '/visit');
    var reqBody = { user_agent: userAgent,
	domain: host,
	path: pathn,
	id: user_id,
	is_new: isNewUser
    };
    var req = new XMLHttpRequest();
    req.open('POST', url);
    req.setRequestHeader('Content-Type', 'application/json; charset=utf-8')
    req.send(JSON.stringify(reqBody));

function uuidv4() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

function findCookieUserId(cookie) {
    if (cookie.length == 0 || cookie == null)
        return null;
    var cookies = cookie.split(';');
    for(var i=0; cookies.length; i++){
        if (cookies[i].split('=')[0] == 'user_id')
            return cookies[i].split('=')[1];
    }
    return null;
}
