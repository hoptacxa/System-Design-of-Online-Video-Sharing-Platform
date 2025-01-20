export class ResponseCommand {
    constructor(
        public readonly peerId: string,
        public readonly to: string,
        public readonly payload: any,
    ) { }
}
