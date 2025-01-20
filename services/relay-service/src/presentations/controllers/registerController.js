const { users, peers } = require('../../data/users.js');

function registerController(ws, data) {
    const { peerId, accessKeyId, accessSecretKey } = data;

    // Xác thực user
    const user = users[accessKeyId];
    if (!user || user.accessSecretKey !== accessSecretKey) {
        ws.send(JSON.stringify({ type: 'error', message: 'Invalid credentials' }));
        return;
    }

    // Kiểm tra quyền sở hữu peer
    if (!user.peers.includes(peerId)) {
        ws.send(JSON.stringify({ type: 'error', message: 'Unauthorized peer' }));
        return;
    }

    // Lưu thông tin peer
    peers[peerId] = { userId: accessKeyId, socket: ws };
    console.log(`Peer registered: ${peerId} (User: ${accessKeyId})`);

    ws.send(JSON.stringify({ type: 'success', message: 'Peer registered successfully' }));
}

module.exports = registerController;
