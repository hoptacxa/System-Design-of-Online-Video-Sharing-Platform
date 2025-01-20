export class RegisterCommand {
    constructor(
        public readonly peerId: string,
        public readonly accessKeyId: string,
        public readonly accessSecretKey: string,
        public readonly storageCapacity: string,
        public readonly peerAddress: string
    ) {}
}
