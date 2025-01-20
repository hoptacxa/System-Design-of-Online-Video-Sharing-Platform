export class ConnectedPeers {
    constructor(public peers: Set<any>) {
        if (!Array.isArray(peers)) {
            throw new Error('ConnectedPeers must be initialized with an array');
        }
        this.peers = new Set(peers);
    }

    addPeer(peerId) {
        this.peers.add(peerId);
    }

    removePeer(peerId) {
        if (!this.peers.has(peerId)) {
            throw new Error(`Peer ${peerId} is not connected`);
        }
        this.peers.delete(peerId);
    }

    getPeers() {
        return Array.from(this.peers);
    }

    equals(other) {
        if (!(other instanceof ConnectedPeers)) return false;
        return this.peers.size === other.peers.size && [...this.peers].every(peer => other.peers.has(peer));
    }
}
