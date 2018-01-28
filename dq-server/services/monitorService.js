
module.exports = function(io) {



    io.on('connection', (socket) => {

        // incr = 0;
        var sendData = function() {
            getAttributes().then(function (data) {
                if (data) {
                    socket.emit('rickshaw', data);
                    // incr++;
                    }
            })
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
        // socket.emit('rickshaw', data);
            
        }
        var run = setInterval(sendData, 1000);

      socket.on('disconnect', ()=> {
        clearInterval(run);
        });
    });    

    
}

const r = require('rethinkdb');

const rethinkdb = {
    host: '34.209.184.21',
    port: 28015,
    authKey: '',
    db: 'test'
}



var connection = null;

r.connect(rethinkdb, function(err, conn) {
    if (err) throw err;
    connection = conn;
})

const getAttributes = function() {
        return new Promise((resolve, reject) => {
            r.table('test_new_stream').changes()("new_val")
            .run(connection, function(err, cursor) {
                if (err) {
                    reject(err);
                } else {
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
                        if (err) throw err;
                        var time = data['time'];
                        var attribute = data['attribute'];
                        // console.log(attribute)
                        attribute.forEach(element => {
                            if (element['name'] === 'a') {
    
                                result[0]["data"].push({'x': (new Date).getTime(), 'y': + element['count']});
                                result[1]["data"].push({'x': (new Date).getTime(), 'y': + element['max']});
                                result[2]["data"].push({'x': (new Date).getTime(), 'y': + element['min']});
                                result[3]["data"].push({'x': (new Date).getTime(), 'y': + element['stddev']});
                                result[4]["data"].push({'x': (new Date).getTime(), 'y': + element['mean']});
                                
                            }
                        });
                        resolve(result);    
                    });
                    
                }            
            

        })
    })
}

// module.exports = {
//     getAttributes
// }