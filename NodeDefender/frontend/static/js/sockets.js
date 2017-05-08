var groupSocket = io.connect('http://' + document.domain + ':' + location.port + '/group');  
var nodeSocket = io.connect('http://' + document.domain + ':' + location.port + '/node'); 
var userSocket = io.connect('http://' + document.domain + ':' + location.port + '/user'); 
var iCPESocket = io.connect('http://' + document.domain + ':' + location.port + '/icpe');
var generalSocket = io.connect('http://' + document.domain + ':' + location.port + '/general');
var adminSocket = io.connect('http://' + document.domain + ':' + location.port + '/admin');
var dataSocket = io.connect('http://' + document.domain + ':' + location.port + '/data');
var plotlySocket = io.connect('http://' + document.domain + ':' + location.port + '/plotly');
var sensorSocket = io.connect('http://' + document.domain + ':' + location.port + '/sensor');

generalSocket.on('reload', function() {
	location.reload();
})

generalSocket.on('redirect', function(url) {
	location.href = url;
});

generalSocket.on('error', function(msg) {
	toastr.error(msg)
});
