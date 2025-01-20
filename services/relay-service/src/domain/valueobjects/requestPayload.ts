export class RequestPayload {
    private readonly data: any;

    constructor(data: any) {
        if (typeof data !== 'object' || data === null) {
            throw new Error('Payload must be a non-null object');
        }
        this.data = data;
    }

    getData(): any {
        return this.data;
    }
}
