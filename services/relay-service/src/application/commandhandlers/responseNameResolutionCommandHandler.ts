import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { ResponseNameResolutionCommand } from '../commands/responseNameResolutionCommand';
import { WebsocketGateway } from '../../presentations/gateways/websocket.gateway';
import { InMemoryRequestReadRepository } from '../../infrastructure/repositories/inMemoryRequestReadRepository';
import { InMemoryRequestWriteRepository } from '../../infrastructure/repositories/inMemoryRequestWriteRepository';
import { RequestUuid } from '../../domain/valueobjects/requestUuid';
import { RequestStatus } from '../../domain/aggregates/requestAggregate';

@CommandHandler(ResponseNameResolutionCommand)
export class ResponseNameResolutionCommandHandler implements ICommandHandler<ResponseNameResolutionCommand> {
    constructor(
        private readonly websocketGateway: WebsocketGateway,
        private readonly inMemoryRequestWriteRepository: InMemoryRequestWriteRepository,
        private readonly inMemoryRequestReadRepository: InMemoryRequestReadRepository,
    ) { }
    async execute(command: ResponseNameResolutionCommand): Promise<any> {
        const {
            cid,
            requestUuid,
        } = command;

        // Logic to validate and forward the response
        if (!this.isPeerAvailable()) {
            throw new Error('Requester peer not found');
        }
        // console.log('respond ', Body)

        this.saveResponse(requestUuid, cid);

        this.forwardResponse(requestUuid, cid);
        return { message: 'Response forwarded successfully' };
    }

    private isPeerAvailable(): boolean {
        // Add your validation logic
        return true; // Placeholder
    }

    private async saveResponse(requestUuid: string, cid: string) {
        if (cid) {
            let request = await this.inMemoryRequestWriteRepository.findById(new RequestUuid(requestUuid));
            request.updateStatus(RequestStatus.COMPLETED)
            this.inMemoryRequestWriteRepository.save(request)
        }
    }
    private forwardResponse(requestUuid, cid) {
        // Add your logic to forward the response
        let request = this.inMemoryRequestReadRepository.getByUuid(requestUuid)
        let requesterId = request.requesterId
        let clients = this.websocketGateway.getClients(requesterId)
        for (let i = 0; i < clients.length; i++) {
            let client = clients[i];
            if (client) {
                client.emit("name-resolved", { cid, requesterId, requestUuid });
            } else {
                throw new Error(`Client with nodeId ${requesterId} not found`);
            }
        }
    }
}