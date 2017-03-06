var groupSocket = io.connect('http://' + document.domain + ':' + location.port + '/group');  
var nodeSocket = io.connect('http://' + document.domain + ':' + location.port + '/node'); 
var userSocket = io.connect('http://' + document.domain + ':' + location.port + '/user'); 
var iCPESocket = io.connect('http://' + document.domain + ':' + location.port + '/icpe');
