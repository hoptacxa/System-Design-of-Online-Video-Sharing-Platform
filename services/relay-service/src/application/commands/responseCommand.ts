export class ResponseCommand {
    constructor(
        public readonly requestUuid: string,
        public readonly Body: any,
    ) { }
}
