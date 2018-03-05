const r = require('rethinkdb');
const rethinkdb = require('./config');


module.exports = function(io) {

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
            
            r.connect(rethinkdb, function(err, conn) {
                if (err) throw err;
                connection = conn;
                console.log(key);
                r.table(key).changes()("new_val")
                .run(connection, function (err, cursor){
                    cursor.each(function(err, data) {                    
                        if (err) throw err;
                        else {
                            var time = data['time'];
                            const now = (new Date).getTime() / 1000;
                            var element = data['summary'];
                            console.log(element);
                            io.in(key).emit(key, element);                                    
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
