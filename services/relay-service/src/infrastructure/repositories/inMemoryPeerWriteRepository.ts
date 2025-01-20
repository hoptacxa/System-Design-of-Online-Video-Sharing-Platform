import { NodeId } from '../../domain/valueobjects/nodeId';
import { PeerAddress } from '../../domain/valueobjects/peerAddress';
import { StorageCapacity } from '../../domain/valueobjects/storageCapacity';
import { ConnectedPeers } from '../../domain/valueobjects/connectedPeers';

export class InMemoryPeerWriteRepository {
    public peers: Map<string, { peerAddress: PeerAddress; storageCapacity: StorageCapacity; connectedPeers: ConnectedPeers }>;

    constructor(sharedPeers: Map<string, { peerAddress: PeerAddress; storageCapacity: StorageCapacity; connectedPeers: ConnectedPeers }>) {
        this.peers = sharedPeers; // Shared datastore
    }

    /**
     * Adds a new peer to the repository.
     * @param {NodeId} nodeId - The unique identifier of the peer.
     * @param {PeerAddress} peerAddress - The address of the peer.
     * @param {StorageCapacity} storageCapacity - The storage capacity of the peer.
     * @throws {Error} If the peer already exists.
     */
    async addPeer(nodeId: NodeId, peerAddress, storageCapacity: StorageCapacity) {
        if (this.peers.has(nodeId.value)) {
            throw new Error(`Peer with nodeId ${nodeId.value} already exists`);
        }
        this.peers.set(nodeId.value, {
            peerAddress,
            storageCapacity,
            connectedPeers: new ConnectedPeers(new Set),
        });
    }

    /**
     * Updates an existing peer's address.
     * @param {NodeId} nodeId - The unique identifier of the peer.
     * @param {PeerAddress} newAddress - The updated address of the peer.
     * @throws {Error} If the peer does not exist.
     */
    async updatePeerAddress(nodeId: NodeId, newAddress: PeerAddress) {
        const peer = this.peers.get(nodeId.value);
        if (!peer) {
            throw new Error(`Peer with nodeId ${nodeId.value} does not exist`);
        }
        peer.peerAddress = newAddress;
        this.peers.set(nodeId.value, peer);
    }

    /**
     * Updates the storage capacity of an existing peer.
     * @param {NodeId} nodeId - The unique identifier of the peer.
     * @param {StorageCapacity} newCapacity - The updated storage capacity.
     * @throws {Error} If the peer does not exist.
     */
    async updateStorageCapacity(nodeId, newCapacity) {
        const peer = this.peers.get(nodeId.value);
        if (!peer) {
            throw new Error(`Peer with nodeId ${nodeId.value} does not exist`);
        }
        peer.storageCapacity = newCapacity;
        this.peers.set(nodeId.value, peer);
    }

    /**
     * Removes a peer from the repository.
     * @param {NodeId} nodeId - The unique identifier of the peer.
     * @throws {Error} If the peer does not exist.
     */
    async removePeer(nodeId) {
        if (!this.peers.has(nodeId.value)) {
            throw new Error(`Peer with nodeId ${nodeId.value} does not exist`);
        }
        this.peers.delete(nodeId.value);
    }
}
