const { peers } = require('../../data/users');

function requestController(ws, data) {
    const { peerId, to, payload } = data;

    if (!peers[peerId]) {
        ws.send(JSON.stringify({ type: 'error', message: 'Requester peer not registered' }));
        return;
    }

    const provider = peers[to];
    if (!provider) {
        ws.send(JSON.stringify({ type: 'error', message: 'Provider peer not found' }));
        return;
    }

    provider.socket.send(JSON.stringify({
        type: 'data-request',
        from: peerId,
        payload,
    }));
}

module.exports = requestController;