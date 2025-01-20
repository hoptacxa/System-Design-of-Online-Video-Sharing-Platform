export class RequestCommand {
    constructor(
      public readonly uuid: string,
      public readonly requesterId: string,
      public readonly providerId: string,
      public readonly payload: any,
    ) {}
  }