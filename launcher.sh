service redis_6379 start
cd dq-server
npm install
nodemon server.js &
cd dq-client
npm install
ng build --watch &

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

service redis_6379 stop

