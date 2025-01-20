import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { ResponseCommand } from '../commands/responseCommand';

@CommandHandler(ResponseCommand)
export class ResponseCommandHandler implements ICommandHandler<ResponseCommand> {
    async execute(command: ResponseCommand): Promise<any> {
        const { peerId, to, payload } = command;

        // Logic to validate and forward the response
        if (!this.isPeerAvailable(to)) {
            throw new Error('Requester peer not found');
        }

        this.forwardResponse(to, { from: peerId, payload });
        return { message: 'Response forwarded successfully' };
    }

    private isPeerAvailable(peerId: string): boolean {
        // Add your validation logic
        return true; // Placeholder
    }

    private forwardResponse(peerId: string, data: any): void {
        // Add your logic to forward the response
    }
}