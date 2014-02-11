var http = require('http');
var url = require('url');
var util = require('util');
var fs = require('fs');

var today = new Date();
var m = (today.getMonth()+1) > 9 ? (today.getMonth()+1) : ('0'+(today.getMonth()+1));
var d = today.getDate() > 9 ? today.getDate() : ('0'+today.getDate());
var logFileName = 'api'+today.getFullYear()+m+d+'.log';

http.createServer( function(req, res){
	console.log('===================request: ', req.method, req.url);

	var urlObject = url.parse(req.url);
	var hostArray = req.headers.host.split(":");
    
    function logFilter() {
        return (urlObject.pathname.indexOf('/api/')>-1);
    }

	var option = {
		'host': hostArray[0],
        'port': Number(hostArray[1]||'80'),
		'path': urlObject.pathname + (urlObject.search||""),
		'method': req.method,
		'headers': req.headers
	};
    //console.log('===================option: ' + util.inspect(option));
    if (logFilter()){
    	fs.appendFile(logFileName, '\nRequest:\t'+option.method+'\t'+option.path+'\t');
	}

    var clientReq = http.request(option, function(clientRes){
    	console.log('===================response: ', clientRes.statusCode);
		res.writeHeader(clientRes.statusCode, clientRes.headers);
		if (logFilter()){
    		fs.appendFile(logFileName, '\nResponse:\t'+option.method+'\t'+option.path+'\t');
		}
        clientRes.on('data', function(chunk){  
        	if (logFilter()){
    			fs.appendFile(logFileName, chunk);
			}
        	res.write(chunk); 
        });
        clientRes.on('end', function(){ 

        	res.end(); 
        });
    });
    clientReq.on('error', function(e){
        console.log(e);
    });

    req.on('data', function(chunk){ 
    	if (logFilter()){
    		fs.appendFile(logFileName, chunk);
		}
    	clientReq.write(chunk); 
    });
    req.on('end',function(){ 
    	clientReq.end();
    });
}).listen(3333);
