const io = require('socket.io-client'); // socket io
const websocket_backend = process.env.VUE_APP_WEBSOCKET_SERVER
console.info(`App is running on: "${process.env.VUE_APP_ENVIRONMENT}" environment...`)
export const socket = io(websocket_backend, {transports: ['websocket',]}) // Flask server address