class User {
    constructor(id, secretKey, peers = []) {
        this.id = id;
        this.secretKey = secretKey;
        this.peers = peers; // Danh sách Peer ID
    }

    // Kiểm tra nếu user sở hữu một peer
    ownsPeer(peerId) {
        return this.peers.includes(peerId);
    }
}

module.exports = User;