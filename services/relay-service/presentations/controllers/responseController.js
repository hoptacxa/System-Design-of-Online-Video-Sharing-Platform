const { peers } = require('../../data/users');

function responseController(ws, data) {
    const { peerId, to, payload } = data;

    const requester = peers[to];
    if (!requester) {
        ws.send(JSON.stringify({ type: 'error', message: 'Requester peer not found' }));
        return;
    }

    requester.socket.send(JSON.stringify({
        type: 'data-response',
        from: peerId,
        payload,
    }));
}

module.exports = responseController;