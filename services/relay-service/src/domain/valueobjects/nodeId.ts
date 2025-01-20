export class NodeId {
    constructor(
        readonly value: any
    ) {
        if (!value || typeof value !== 'string') {
            throw new Error('NodeId must be a non-empty string');
        }
        this.value = value;
    }

    equals(other: any) {
        return other instanceof NodeId && this.value === other.value;
    }
}
