export class RegisterCommand {
    readonly peerId: string;
    readonly accessKeyId: string;
    readonly accessSecretKey: string;
    readonly client: string;

    constructor(peerId: string, accessKeyId: string, accessSecretKey: string, client) {
        this.peerId = peerId;
        this.accessKeyId = accessKeyId;
        this.accessSecretKey = accessSecretKey;
        this.client = client;
    }
}
