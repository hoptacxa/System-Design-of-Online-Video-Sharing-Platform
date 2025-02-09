import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { ResponseCommand } from '../commands/responseCommand';
import { WebsocketGateway } from 'src/presentations/gateways/websocket.gateway';
import { InMemoryRequestReadRepository } from '../../infrastructure/repositories/inMemoryRequestReadRepository';
import { InMemoryRequestWriteRepository } from '../../infrastructure/repositories/inMemoryRequestWriteRepository';
import { RequestUuid } from '../../domain/valueobjects/requestUuid';
import { RequestStatus } from '../../domain/aggregates/requestAggregate';

@CommandHandler(ResponseCommand)
export class ResponseCommandHandler implements ICommandHandler<ResponseCommand> {
    constructor(
        private readonly websocketGateway: WebsocketGateway,
        private readonly inMemoryRequestWriteRepository: InMemoryRequestWriteRepository,
        private readonly inMemoryRequestReadRepository: InMemoryRequestReadRepository,
    ) { }
    async execute(command: ResponseCommand): Promise<any> {
        const {
            Body,
            requestUuid,
        } = command;

        // Logic to validate and forward the response
        if (!this.isPeerAvailable()) {
            throw new Error('Requester peer not found');
        }
        // console.log('respond ', Body)

        this.saveResponse(requestUuid, Body);

        this.forwardResponse(requestUuid, Body);
        return { message: 'Response forwarded successfully' };
    }

    private isPeerAvailable(): boolean {
        // Add your validation logic
        return true; // Placeholder
    }

    private async saveResponse(requestUuid: string, Body: string) {
        if (Body) {
            let request = await this.inMemoryRequestWriteRepository.findById(new RequestUuid(requestUuid));
            request.updateStatus(RequestStatus.COMPLETED)
            this.inMemoryRequestWriteRepository.save(request)
        }
    }
    private forwardResponse(requestUuid, Body) {
        // Add your logic to forward the response
        let request = this.inMemoryRequestReadRepository.getByUuid(requestUuid)
        let requesterId = request.requesterId
        let clients = this.websocketGateway.getClients(requesterId)
        for (let i = 0; i < clients.length; i++) {
            let client = clients[i];
            if (client) {
                client.emit("response", { Body, requesterId, requestUuid });
            } else {
                throw new Error(`Client with nodeId ${requesterId} not found`);
            }
        }
    }
}