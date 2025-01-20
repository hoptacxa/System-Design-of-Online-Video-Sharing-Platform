export class PeerAddress {
    constructor(public value: any) {
        if (!value || typeof value !== 'string' || !this.isValidAddress(value)) {
            throw new Error('Invalid PeerAddress');
        }
        this.value = value;
    }

    isValidAddress(value) {
        // Simplified validation: Extend with specific logic for IP or multiaddress formats
        return value.includes('.') || value.startsWith('/');
    }

    equals(other) {
        return other instanceof PeerAddress && this.value === other.value;
    }
}
