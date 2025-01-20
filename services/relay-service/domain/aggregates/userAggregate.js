const User = require('../entities/user');
const Peer = require('../entities/peer');

class UserAggregate {
    constructor(user, peers = []) {
        if (!(user instanceof User)) {
            throw new Error('Invalid User entity');
        }

        this.user = user; // Thực thể User
        this.peers = peers; // Danh sách các thực thể Peer
    }

    // Thêm Peer vào Aggregate
    addPeer(peer) {
        if (!(peer instanceof Peer)) {
            throw new Error('Invalid Peer entity');
        }

        if (peer.userId !== this.user.id) {
            throw new Error('Peer does not belong to this User');
        }

        this.peers.push(peer);
    }

    // Tìm Peer theo ID
    findPeerById(peerId) {
        return this.peers.find((peer) => peer.id === peerId) || null;
    }

    // Kiểm tra nếu User sở hữu một Peer
    ownsPeer(peerId) {
        return this.user.ownsPeer(peerId);
    }
}

module.exports = UserAggregate;