
const r = require('rethinkdb');

const rethinkdb = {
    host: '34.209.184.21',
    port: 28015,
    authKey: '',
    db: 'test'
}

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
    


        r.connect(rethinkdb, function(err, conn) {
            if (err) throw err;
            connection = conn;
            return r.table('test_new_stream').changes()("new_val")
            .run(connection, function (err, cursor){
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
                cursor.each(function(err, data) {                    
                    if (err) reject(err);
                    else {
                        var time = data['time'];
                        var attribute = data['attribute'];
                        attribute.forEach(element => {
                            if (element['name'] === 'a') {
                                const now = (new Date).getTime() / 1000;
                                result[0]["data"].push({'x': now, 'y': + element['count']});
                                result[1]["data"].push({'x': now, 'y': + element['max']});
                                result[2]["data"].push({'x': now, 'y': + element['min']});
                                result[3]["data"].push({'x': now, 'y': + element['stddev']});
                                result[4]["data"].push({'x': now, 'y': + element['mean']});                            
                            }
                        });
                        console.log(result[0]["data"].length);
                        console.log(result[0]["data"]);
                        if (result[0]["data"].length > 100) {
                            result[0]["data"].shift();
                            result[1]["data"].shift();
                            result[2]["data"].shift();
                            result[3]["data"].shift();
                            result[4]["data"].shift();                        
                        }   
                        socket.emit('rickshaw', result);    
                        socket.emit('a', result);    
                        
                    }                    
                });
                
            }).catch(function(error) {                
                console.log('An error occur', error);
                return Promise.reject(error);})
        })
    })


}
