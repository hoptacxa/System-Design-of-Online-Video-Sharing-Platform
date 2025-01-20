const WebSocket = require('ws');
const routeMessage = require('./presentations/routes/message.js');

const PORT = 8080;
const wss = new WebSocket.Server({ port: PORT });

const { peers } = require('./data/users');

wss.on('connection', (ws) => {
    console.log('New client connected');

    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message);
            routeMessage(ws, data);
        } catch (err) {
            ws.send(JSON.stringify({ type: 'error', message: 'Invalid JSON format' }));
        }
    });

    ws.on('close', () => {
        for (let peerId in peers) {
            if (peers[peerId].socket === ws) {
                console.log(`Peer disconnected: ${peerId}`);
                delete peers[peerId];
                break;
            }
        }
    });
});

console.log(`Server running on ws://localhost:${PORT}`);
