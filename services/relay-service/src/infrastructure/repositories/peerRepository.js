const { peers } = require('../database');
const Peer = require('../../domain/entities/peer');

class PeerRepository {
    addPeer(peerEntity) {
        if (!(peerEntity instanceof Peer)) {
            throw new Error('Invalid Peer entity');
        }

        peers[peerEntity.id] = {
            userId: peerEntity.userId,
            socket: peerEntity.socket,
        };
    }

    findPeerById(peerId) {
        const peerData = peers[peerId];
        if (!peerData) return null;

        return new Peer(peerId, peerData.userId, peerData.socket);
    }

    removePeer(peerId) {
        delete peers[peerId];
    }
}

module.exports = PeerRepository;