class Peer {
    constructor(id, userId, socket) {
        this.id = id;
        this.userId = userId; // User sở hữu Peer
        this.socket = socket; // WebSocket kết nối với Peer
    }
}

module.exports = Peer;