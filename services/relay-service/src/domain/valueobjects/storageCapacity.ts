export class StorageCapacity {
    constructor(public value: any) {
        if (typeof value !== 'number' || value < 0) {
            throw new Error('StorageCapacity must be a non-negative number');
        }
        this.value = value;
    }

    equals(other) {
        return other instanceof StorageCapacity && this.value === other.value;
    }
}
