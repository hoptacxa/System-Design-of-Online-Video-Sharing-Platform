export class InMemoryPeerWriteRepository {
    public peers: Map<string, any>;
    constructor(sharedPeers: Map<string, any>) {
        this.peers = sharedPeers; // Shared datastore
    }

    /**
     * Adds a new peer to the repository.
     * @param {string} nodeId - The unique identifier of the peer.
     * @param {object} peerData - The peer data (e.g., address, storageCapacity).
     * @throws {Error} If the peer already exists.
     */
    async addPeer(nodeId, peerData) {
        if (this.peers.has(nodeId)) {
            throw new Error(`Peer with nodeId ${nodeId} already exists`);
        }
        this.peers.set(nodeId, peerData);
    }

    /**
     * Updates an existing peer's data.
     * @param {string} nodeId - The unique identifier of the peer.
     * @param {object} updatedData - The updated peer data.
     * @throws {Error} If the peer does not exist.
     */
    async updatePeer(nodeId, updatedData) {
        if (!this.peers.has(nodeId)) {
            throw new Error(`Peer with nodeId ${nodeId} does not exist`);
        }
        const existingPeer = this.peers.get(nodeId);
        this.peers.set(nodeId, { ...existingPeer, ...updatedData });
    }

    /**
     * Removes a peer from the repository.
     * @param {string} nodeId - The unique identifier of the peer.
     * @throws {Error} If the peer does not exist.
     */
    async removePeer(nodeId) {
        if (!this.peers.has(nodeId)) {
            throw new Error(`Peer with nodeId ${nodeId} does not exist`);
        }
        this.peers.delete(nodeId);
    }
}
