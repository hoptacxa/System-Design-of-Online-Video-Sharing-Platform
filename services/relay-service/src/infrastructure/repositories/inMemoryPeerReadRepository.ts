export class InMemoryPeerReadRepository {
    public peers: Map<string, any>;
    constructor(sharedPeers) {
        this.peers = sharedPeers; // Shared datastore
    }

    /**
     * Retrieves a peer by its nodeId.
     * @param {string} nodeId - The unique identifier of the peer.
     * @returns {object|null} The peer data or null if not found.
     */
    async getPeer(nodeId) {
        return this.peers.get(nodeId) || null;
    }

    /**
     * Retrieves all peers in the repository.
     * @returns {Array<object>} An array of all peers' data.
     */
    async getAllPeers() {
        return Array.from(this.peers.values());
    }

    /**
     * Checks if a peer exists in the repository.
     * @param {string} nodeId - The unique identifier of the peer.
     * @returns {boolean} True if the peer exists, otherwise false.
     */
    async peerExists(nodeId) {
        return this.peers.has(nodeId);
    }
}