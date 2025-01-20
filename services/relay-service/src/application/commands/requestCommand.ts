export class RequestCommand {
    constructor(
      public readonly peerId: string,
      public readonly to: string,
      public readonly payload: any,
    ) {}
  }