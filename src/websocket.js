const io = require('socket.io-client'); // socket io

export const socket = io('ws://localhost:5000', {transports: ['websocket',]}) // Flask server address