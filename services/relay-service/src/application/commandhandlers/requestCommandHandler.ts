import { CommandHandler, ICommandHandler } from '@nestjs/cqrs';
import { RequestCommand } from '../commands/requestCommand';
import { RequestAggregate, RequestStatus } from '../../domain/aggregates/requestAggregate';
import { InMemoryRequestWriteRepository } from '../../infrastructure/repositories/inMemoryRequestWriteRepository';
import { InMemoryRequestReadRepository } from '../../infrastructure/repositories/inMemoryRequestReadRepository';
import { InMemoryPeerReadRepository } from '../../infrastructure/repositories/inMemoryPeerReadRepository';
import { RequestUuid } from '../../domain/valueobjects/requestUuid';
import { NodeId } from '../../domain/valueobjects/nodeId';
import { RequestPayload } from '../../domain/valueobjects/requestPayload';
import { WebsocketGateway } from '../../presentations/gateways/websocket.gateway';

@CommandHandler(RequestCommand)
export class RequestCommandHandler implements ICommandHandler<RequestCommand> {
    constructor(
        private readonly inMemoryPeerReadRepository: InMemoryPeerReadRepository,
        private readonly websocketGateway: WebsocketGateway,
        private readonly inMemoryRequestReadRepository: InMemoryRequestReadRepository,
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
        setTimeout(async () => {
            let request = this.inMemoryRequestReadRepository.getByUuid(uuid)
            console.log('request')
            if (request.status === RequestStatus.PENDING) {
                console.log('is pending')
                let clientsMap = this.websocketGateway.getAllClients();
                for (const [clientKey, clients] of clientsMap.entries()){
                    console.log(clientKey)
                    for (let i = 0; i < clients.length; i++) {
                        const client = clients[i];
                        console.log('payload', client, payload)
                        // client.emit("responder-not-found", payload);
                    }
                }
            }
        }, 10e3);
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
        let clients = this.websocketGateway.getClients(providerId)
        if (typeof clients === 'undefined') {
            console.log("No clients available")
            return false;
        }
        for (let i = 0; i < clients.length; i++) {
            const client = clients[i];
            client.emit("request", {payload, requesterId, uuid});
        }
    }
}