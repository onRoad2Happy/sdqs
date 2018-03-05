const express = require('express');
const app = express();


const restRouter = require('./routes/rest');
const indexRouter = require('./routes/index');
const path = require('path');

app.use(express.static(path.join(__dirname, '../public/')));

app.use('/', indexRouter);
app.use('/api/v1', restRouter);

app.use(function(req, res) {
  res.sendFile('index.html', {root: path.join(__dirname, '../public')});
});

// app.listen(3000, () => console.log('Example app listening on port 3000!'));

const http = require('http');
const socketIO = require('socket.io');

const redis = require('socket.io-redis');

const io = socketIO(http);

const monitorSocketService = require('./services/monitorService.js')(io);
const profileSocketService = require('./services/profileService.js')(io);

const server = http.createServer(app);
io.attach(server);
io.adapter(redis({host:'localhost', port:6379}))
server.listen(3000);
server.on('error', onError);
server.on('listening', onListening);

function onError(error) {
  console.log(error)
  throw error;
}

function onListening() {
  const address = server.address();
  const bind = typeof address === 'string' ? 'pipe ' + address : 'port' + address.port;
  console.log('Listening on ' + bind);
}

