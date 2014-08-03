var http = require('http');
var server = http.createServer().listen(8001);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');

var redis = require('socket.io/node_modules/redis');
var sub = redis.createClient();
 
//Subscribe to the Redis chat channel
sub.subscribe('spire-pusher');

//Configure socket.io to store cookie set by Django
io.configure(function(){
    io.set('authorization', function(data, accept){
        if(data.headers.cookie){
            data.cookie = cookie_reader.parse(data.headers.cookie);
            return accept(null, true);
        }
        return accept('error', false);
    });
    io.set('log level', 1);
});

io.sockets.on('connection', function (socket) {

    //Grab message from Redis and send to client
    sub.on('message', function(channel, message){
        console.log(message);
        // TODO: update the DOM to show the blimp is ready
    });

});
