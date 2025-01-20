const registerRoute = require('./register');
const requestRoute = require('./request');
const responseRoute = require('./response');

function routeMessage(ws, data) {
    switch (data.type) {
        case 'register':
            registerRoute(ws, data);
            break;
        case 'request':
            requestRoute(ws, data);
            break;
        case 'response':
            responseRoute(ws, data);
            break;
        default:
            console.log('Unknown message type:', data.type);
            ws.send(JSON.stringify({ type: 'error', message: 'Unknown message type' }));
    }
}

module.exports = routeMessage;