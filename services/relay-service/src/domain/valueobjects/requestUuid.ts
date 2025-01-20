import { validate as validateUuid } from 'uuid';

export class RequestUuid {
    private readonly value: string;

    constructor(value: string) {
        if (!validateUuid(value)) {
            throw new Error('Invalid UUID format');
        }
        this.value = value;
    }

    getValue(): string {
        return this.value;
    }
}