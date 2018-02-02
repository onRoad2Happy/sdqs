const r = require('rethinkdb');

const rethinkdb = require('./config');
// result = [
//     {
//         "color": "#ff8df5",
//         "name": 'count',
//         "data": []
//     },
//     {
//         "color": "#fdd4ed",
//         "name": 'max',
//         "data": []
//     },
//     {
//         "color": "#ffe38d",
//         "name": 'min',
//         "data": []
//     },
//     {
//         "color": "#ffeea5",
//         "name": 'stddev',
//         "data": []
//     },
//     {
//         "color": "#ffd381",
//         "name": 'mean',
//         "data": []
//     },        
// ]

module.exports = function(io) {
    io.on('connection', (socket)=> {    
        // incr = 0;
        // var sendData = function() {
        //     data = [
        //         {
        //             "color": "blue",
        //             "name": "New York",
        //             "data": [ { "x": 0, "y": incr }, { "x": 1, "y": 49 }, { "x": 2, "y": 38 }, { "x": 3, "y": 30 }, { "x": 4, "y": 32 } ]
        //         }, {
        //           "color": "red",
        //             "name": "London",
        //             "data": [ { "x": 0, "y": 19 }, { "x": 1, "y": incr }, { "x": 2, "y": 29 }, { "x": 3, "y": 20 }, { "x": 4, "y": 14 } ]
        //         }, {
        //           "color": "black",
        //             "name": "Tokyo",
        //             "data": [ { "x": 0, "y": 8 }, { "x": 1, "y": 12 }, { "x": 2, "y": incr }, { "x": 3, "y": 11 }, { "x": 4, "y": 10 } ]
        //         }
        //   ]
        //     socket.emit('rickshaw', data);
        //     incr++;
        // }
        // var run = setInterval(sendData, 1000);
        //   socket.on('disconnect', function() {
        //     clearInterval(run);
        // });
        // const attr = socket.handshake.query['attributeId'];
        result = [
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
        // socket.on('room', function(room) {
        //     console.log('join room' + room);
        //     socket.join(room);
        // })

        socket.on('getData', function(key) {            
            
            r.connect(rethinkdb, function(err, conn) {
                if (err) throw err;
                connection = conn;
                r.table('test_topic').changes()("new_val")
                .run(connection, function (err, cursor){
                    cursor.each(function(err, data) {                    
                        if (err) throw err;
                        else {
                            var time = data['time'];
                            const now = (new Date).getTime() / 1000;
                                var element = data['summary'][key];
                                result[0]["data"].push({'x': now, 'y': + element['count']});
                                result[1]["data"].push({'x': now, 'y': + element['max']});
                                result[2]["data"].push({'x': now, 'y': + element['min']});
                                result[3]["data"].push({'x': now, 'y': + element['stddev']});
                                result[4]["data"].push({'x': now, 'y': + element['mean']});                            
                                if (result[0]["data"].length > 20) {
                                    result[0]["data"].shift();
                                    result[1]["data"].shift();
                                    result[2]["data"].shift();
                                    result[3]["data"].shift();
                                    result[4]["data"].shift();                        
                                }   
                                console.log(key);
                                console.log(result[0]["data"].length);
                                // console.log(result);
                                // io.in(key).emit(key, result);
                                io.emit(key, result);
                                // socket.in(key).emit(key, result);                                                                                
                                // io.sockets.in(key).emit(key, result);
                        }                    
                    });

                    socket.on('disconnect', function() {
                        cursor.close(function(err) {                            
                            if (err) {
                                console.log("An error occurred on cursor close");
                            }
                        })
                        conn.close();
                    })
                    
                }).catch(function(error) {                
                    console.log('An error occur', error);
                    return Promise.reject(error);})

                
            }).catch(function(error) {                
                console.log('An error occur', error);
                return Promise.reject(error);})
        })

    })


}
