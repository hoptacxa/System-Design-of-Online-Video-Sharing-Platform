import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { RequestCommand } from '../commands/requestCommand';
import { RequestAggregate } from 'src/domain/aggregates/requestAggregate';
import { InMemoryRequestWriteRepository } from '../infrastructure/repositories/inMemoryRequestWriteRepository';
import { InMemoryPeerReadRepository } from 'src/infrastructure/repositories/inMemoryPeerReadRepository';
import { RequestUuid } from 'src/domain/valueobjects/requestUuid';
import { NodeId } from 'src/domain/valueobjects/nodeId';
import { RequestPayload } from 'src/domain/valueobjects/requestPayload';
import { WebsocketGateway } from 'src/presentations/gateways/websocket.gateway';

@CommandHandler(RequestCommand)
export class RequestCommandHandler implements ICommandHandler<RequestCommand> {
    constructor(
        private readonly inMemoryPeerReadRepository: InMemoryPeerReadRepository,
        private readonly websocketGateway: WebsocketGateway,
        private readonly inMemoryRequestWriteRepository: InMemoryRequestWriteRepository
    ) {}
    async execute(command: RequestCommand): Promise<any> {
        const { requesterId, providerId, payload, uuid } = command;

        // Logic to validate and forward the request
        if (!this.isPeerRegistered(requesterId)) {
            throw new Error('Requester peer not registered');
        }

        if (!this.isPeerAvailable(providerId)) {
            throw new Error('Provider peer not found');
        }
        this.saveRequest(uuid, requesterId, providerId, payload);

        this.forwardRequest(providerId, requesterId, uuid, payload);
        return { message: 'Request processed successfully', uuid }
    }

    private isPeerRegistered(peerId: string): boolean {
        // Add your validation logic
        return true; // Placeholder
    }

    private isPeerAvailable(peerId: string): boolean {
        // Add your validation logic
        return true; // Placeholder
    }

    private saveRequest(uuid, requesterId, providerId, payload) {
        let request = new RequestAggregate(
            new RequestUuid(uuid),
            new NodeId(requesterId),
            new NodeId(providerId),
            new RequestPayload(payload)
        )
        this.inMemoryRequestWriteRepository.save(request)
    }

    private forwardRequest(providerId, requesterId, uuid, payload) {
        // Add your logic to forward the request
        // console.log({requesterId,providerId, uuid, payload})
        let client = this.websocketGateway.getClient(providerId)
        if (client) {
            client.emit("request", {payload, requesterId, uuid});
        } else {
            throw new Error(`Client with nodeId ${providerId} not found`);
        }
    }
}