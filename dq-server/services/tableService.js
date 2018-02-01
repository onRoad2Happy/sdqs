
// let tables = [
//   {
//       id: 1,
//       name: "table1",
//       attributes: [
//         {
//             name: "attr1",
//             count: 5,
//             max: 5,
//             min: 2,
//             mean: 3,
//             stddev: 2
//           },
//           {
//               name: "attr2",
//             count: 5,
//             max: 9,
//             min: 2,
//             mean: 3,
//             stddev: 2      
//           }
//     ]
// },
//   {
//       id: 2,
//       name: "table2",
//       attributes: [
//         {
//           name: "attr1",
//           count: 5,
//           max: 5,
//           min: 2,
//           mean: 3,
//           stddev: 2
//         },
//         {
//             name: "attr2",
//           count: 5,
//           max: 9,
//           min: 2,
//           mean: 3,
//           stddev: 2      
//         }
//     ]
//   }
// ]

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



const getTables = function() {
    // return new Promise((resolve, reject) => {        
    //   resolve(tables);
    // })

    return new Promise((resolve, reject) => {
        r.table('test_table').run(connection, function(err, cursor) {
            if (err) {
                reject(err);
            } else {
                cursor.toArray(function(err, tables) {
                    if (err) throw err;
                    // console.log(JSON.stringify(result, null, 2));
                    resolve(tables)
                });
            }            
        });
      });
    
}  

const getTable = function(id) {
    // return new Promise((resolve, reject) => {
    //     resolve(tables.find(table => table.id === id));
    // })

    return new Promise((resolve, reject) => {
        r.table('test_table').run(connection, function(err, cursor) {
            if (err) {
                reject(err);
            } else {
                cursor.toArray(function(err, tables) {
                    if (err) throw err;
                    // console.log(JSON.stringify(result, null, 2));  
                    resolve(tables.find(table => table.id === id));
                });
            }            
        });
      });
}


module.exports = {
    getTable,
    getTables
}