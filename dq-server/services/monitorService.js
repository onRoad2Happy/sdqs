const r = require('rethinkdb');
const rethinkdb = require('./config');


module.exports = function(io) {
    result = {};

    io.on('connection', (socket)=> {
        socket.on('join', function(room){
            socket.join(room);
            socket.adapter.clients([room], (err, clients) => {
                console.log(clients);
                if (clients.length === 1) {
                    socket.emit('create_room');
                }
            })            
        }) 
        socket.on('getData', function(key) {            
            
            result[key] = [
                {
                    "color": "#ff8df5",
                    "name": 'count',
                    "data": []
                },
                {
                    "color": "#fdd4ed",
                    "name": 'max',
                    "data": []
                },
                {
                    "color": "#ffe38d",
                    "name": 'min',
                    "data": []
                },
                {
                    "color": "#ffeea5",
                    "name": 'stddev',
                    "data": []
                },
                {
                    "color": "#ffd381",
                    "name": 'mean',
                    "data": []
                },        
            ]
            r.connect(rethinkdb, function(err, conn) {
                if (err) throw err;
                connection = conn;
                r.table('stream').changes()("new_val")
                .run(connection, function (err, cursor){
                    cursor.each(function(err, data) {                    
                        if (err) throw err;
                        else {
                            var time = data['time'];
                            const now = (new Date).getTime() / 1000;
                                var element = data['summary'][key];
                                result[key][0]["data"].push({'x': now, 'y': + element['count']});
                                result[key][1]["data"].push({'x': now, 'y': + element['max']});
                                result[key][2]["data"].push({'x': now, 'y': + element['min']});
                                result[key][3]["data"].push({'x': now, 'y': + element['stddev']});
                                result[key][4]["data"].push({'x': now, 'y': + element['mean']});                            
                                if (result[key][0]["data"].length > 20) {
                                    result[key][0]["data"].shift();
                                    result[key][1]["data"].shift();
                                    result[key][2]["data"].shift();
                                    result[key][3]["data"].shift();
                                    result[key][4]["data"].shift();                        
                                }   
                                
                                io.in(key).emit(key, result[key]);                                    
                                
                        }                    
                    });

                    
                    socket.on('disconnect', function() {
                        console.log('should has leave info');
                        socket.adapter.clients([key], (err, clients) => {
                            console.log(key);
                            console.log('in room has clients');
                            console.log(clients);
                            if (clients.length === 0) {
                                cursor.close(function(err) {
                                    console.log("close connection because last one leave.")                            
                                    if (err) {
                                        console.log("An error occurred on cursor close");
                                    }
                                })
                            }
                        })    
                        
                        // conn.close();
                    })
                    
                }).catch(function(error) {                
                    console.log('An error occur', error);
                    // return Promise.reject(error);
                })

                
            }).catch(function(error) {                
                console.log('An error occur', error);
                // return Promise.reject(error);
            })
        })

    })


}
