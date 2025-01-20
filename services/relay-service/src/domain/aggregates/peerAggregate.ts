import { NodeId } from '../valueobjects/nodeId'
import { PeerAddress } from '../valueobjects/peerAddress'
import { StorageCapacity } from '../valueobjects/storageCapacity'
import { ConnectedPeers } from '../valueobjects/connectedPeers'

export class PeerAggregate {
    constructor(
        public nodeId: NodeId,
        public peerAddress: PeerAddress,
        public storageCapacity: StorageCapacity,
        public connectedPeers: ConnectedPeers,
        public isRegistered = false,
    ) {
    }

    /**
     * Registers the peer.
     */
    register() {
        if (this.isRegistered) {
            throw new Error(`Peer ${this.nodeId.value} is already registered`);
        }
        this.isRegistered = true;
    }

    /**
     * Deregisters the peer.
     */
    deregister() {
        if (!this.isRegistered) {
            throw new Error(`Peer ${this.nodeId.value} is not registered`);
        }
        this.isRegistered = false;
    }

    /**
     * Updates the peer's address.
     * @param {string} newAddress
     */
    updateAddress(newAddress) {
        this.peerAddress = new PeerAddress(newAddress);
    }

    /**
     * Updates the storage capacity.
     * @param {number} newCapacity
     */
    updateStorageCapacity(newCapacity) {
        this.storageCapacity = new StorageCapacity(newCapacity);
    }

    /**
     * Adds a connected peer.
     * @param {string} peerId
     */
    addConnectedPeer(peerId) {
        this.connectedPeers.addPeer(peerId);
    }

    /**
     * Removes a connected peer.
     * @param {string} peerId
     */
    removeConnectedPeer(peerId) {
        this.connectedPeers.removePeer(peerId);
    }

    /**
     * Gets the status of the peer.
     * @returns {object}
     */
    getStatus() {
        return {
            nodeId: this.nodeId.value,
            peerAddress: this.peerAddress.value,
            storageCapacity: this.storageCapacity.value,
            connectedPeers: this.connectedPeers.getPeers(),
            isRegistered: this.isRegistered,
        };
    }
}
