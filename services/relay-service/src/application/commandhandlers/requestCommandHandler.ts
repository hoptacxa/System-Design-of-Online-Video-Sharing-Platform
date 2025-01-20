import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { RequestCommand } from '../commands/requestCommand';

@CommandHandler(RequestCommand)
export class RequestCommandHandler implements ICommandHandler<RequestCommand> {
    async execute(command: RequestCommand): Promise<any> {
        const { peerId, to, payload } = command;

        // Logic to validate and forward the request
        if (!this.isPeerRegistered(peerId)) {
            throw new Error('Requester peer not registered');
        }

        if (!this.isPeerAvailable(to)) {
            throw new Error('Provider peer not found');
        }

        this.forwardRequest(to, { from: peerId, payload });
        return { message: 'Request forwarded successfully' };
    }

    private isPeerRegistered(peerId: string): boolean {
        // Add your validation logic
        return true; // Placeholder
    }

    private isPeerAvailable(peerId: string): boolean {
        // Add your validation logic
        return true; // Placeholder
    }

    private forwardRequest(peerId: string, data: any): void {
        // Add your logic to forward the request
    }
}